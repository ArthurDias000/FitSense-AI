import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


ARQUIVO_BASE = "base_fitsense.csv"
ARQUIVO_MODELO = "modelo_fitsense.pkl"
ARQUIVO_ENCODERS = "encoders_fitsense.pkl"

modelo = None
encoders = {}


def converter_bool(valor):
    valor = str(valor).lower().strip()
    return 1 if valor in ["true", "1", "sim", "yes"] else 0


def treinar_modelo(caminho_arquivo):
    global modelo, encoders

    novo_df = pd.read_csv(caminho_arquivo)

    colunas_obrigatorias = [
        "atraso",
        "satisfacao",
        "personal",
        "freq",
        "tempo",
        "idade",
        "valor",
        "status"
    ]

    for coluna in colunas_obrigatorias:
        if coluna not in novo_df.columns:
            raise ValueError(f"Coluna obrigatória ausente: {coluna}")

    if os.path.exists(ARQUIVO_BASE):
        base_antiga = pd.read_csv(ARQUIVO_BASE)
        base = pd.concat([base_antiga, novo_df], ignore_index=True)
    else:
        base = novo_df.copy()

    if "id_aluno" in base.columns:
        base = base.drop_duplicates(subset=["id_aluno"], keep="last")
    elif "nome" in base.columns:
        base = base.drop_duplicates(subset=["nome"], keep="last")

    base.to_csv(ARQUIVO_BASE, index=False)

    df = base.copy()

    df["satisfacao"] = df["satisfacao"].astype(str).str.lower().str.strip()
    df["atraso"] = df["atraso"].apply(converter_bool)
    df["personal"] = df["personal"].apply(converter_bool)

    df["freq"] = pd.to_numeric(df["freq"])
    df["tempo"] = pd.to_numeric(df["tempo"])
    df["idade"] = pd.to_numeric(df["idade"])
    df["valor"] = pd.to_numeric(df["valor"])

    df["cancelou"] = df["status"].astype(str).str.lower().str.strip().map({
        "ativo": 0,
        "inativo": 1
    })

    if df["cancelou"].isnull().any():
        raise ValueError("A coluna status deve conter apenas 'ativo' ou 'inativo'.")

    encoders = {}

    le_satisfacao = LabelEncoder()
    df["satisfacao"] = le_satisfacao.fit_transform(df["satisfacao"])
    encoders["satisfacao"] = le_satisfacao

    X = df[[
        "atraso",
        "satisfacao",
        "personal",
        "freq",
        "tempo",
        "idade",
        "valor"
    ]]

    y = df["cancelou"]

    modelo = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    modelo.fit(X, y)

    joblib.dump(modelo, ARQUIVO_MODELO)
    joblib.dump(encoders, ARQUIVO_ENCODERS)

    return base


def carregar_modelo():
    global modelo, encoders

    if os.path.exists(ARQUIVO_MODELO):
        modelo = joblib.load(ARQUIVO_MODELO)

    if os.path.exists(ARQUIVO_ENCODERS):
        encoders = joblib.load(ARQUIVO_ENCODERS)


def prever_cancelamento(
    atraso,
    satisfacao,
    personal,
    frequencia,
    tempo_plano,
    idade,
    plano_valor
):
    global modelo, encoders

    if modelo is None:
        carregar_modelo()

    if modelo is None:
        raise Exception("Nenhum modelo treinado. Importe um CSV primeiro.")

    satisfacao = str(satisfacao).lower().strip()

    if satisfacao not in encoders["satisfacao"].classes_:
        raise Exception(f"Satisfação inválida: {satisfacao}")

    satisfacao_cod = encoders["satisfacao"].transform([satisfacao])[0]

    entrada = pd.DataFrame([{
        "atraso": converter_bool(atraso),
        "satisfacao": satisfacao_cod,
        "personal": converter_bool(personal),
        "freq": int(frequencia),
        "tempo": int(tempo_plano),
        "idade": int(idade),
        "valor": float(plano_valor)
    }])

    previsao = modelo.predict(entrada)[0]
    probabilidade = modelo.predict_proba(entrada).max() * 100

    risco = "ALTO" if previsao == 1 else "BAIXO"

    return {
        "risco": risco,
        "probabilidade": round(probabilidade, 2),
        "score": None,
        "detalhes": []
    }