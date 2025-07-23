import pyautogui as pag
from time import sleep
import random
import json

VERDE = (34, 197, 94)
AMARELO = (234, 179, 8)
CINZA = (148, 163, 184)

letras_corretas = [None] * 5
letras_parciais = []
letras_erradas = set()
palavras_usadas = set()

def obter_resultado_do_jogo(linha_index):
    caminho = "pasta_teste/screenshot.png"
    screenshot = pag.screenshot()
    screenshot.save(caminho)

    casas_x = [802, 878, 958, 1033, 1108]
    casas_y = [220, 291, 371, 444, 518, 594]

    y = casas_y[linha_index]
    cores = [screenshot.getpixel((x, y)) for x in casas_x]
    return cores

def interpretar_resultado(palavra, cores):
    resultado = []
    for i, cor in enumerate(cores):
        letra = palavra[i]
        if cor == VERDE:
            resultado.append("🟩")
            letras_corretas[i] = letra
        elif cor == AMARELO:
            resultado.append("🟨")
            if {"letra": letra, "pos": i} not in letras_parciais:
                letras_parciais.append({"letra": letra, "pos": i})
        elif cor == CINZA:
            usada = (
                letra in letras_corretas or
                any(p["letra"] == letra for p in letras_parciais)
            )
            if not usada:
                letras_erradas.add(letra)
            resultado.append("⬜")
        else:
            resultado.append(" ")
    return "".join(resultado)


def filtrar_palavras(lista):
    def valida(palavra):
        for i in range(5):
            if letras_corretas[i] and palavra[i] != letras_corretas[i]:
                return False
        for item in letras_parciais:
            if item["letra"] not in palavra or palavra[item["pos"]] == item["letra"]:
                return False
        for letra in letras_erradas:
            if letra in palavra:
                return False
        return True

    return [p for p in lista if valida(p)]

def escolher_palavra(lista):
    candidatas = [p for p in filtrar_palavras(lista) if p not in palavras_usadas]
    if not candidatas:
        return None
    escolha = random.choice(candidatas)
    palavras_usadas.add(escolha)
    return escolha

def jogar():
    pag.keyDown('alt')

    sleep(0.2)

    pag.press('tab')

    pag.keyUp('alt')
    with open("palavras.json", "r", encoding="utf-8") as arq:
        palavras = json.load(arq)

    for tentativa in range(6):
        palavra = escolher_palavra(palavras)
        if not palavra:
            print("Acabaram as opções possíveis.")
            break

        sleep(1)
        pag.write(palavra, interval=0.3)
        sleep(1)
        pag.press("enter")
        sleep(1)
        cores = obter_resultado_do_jogo(tentativa)
        resultado = interpretar_resultado(palavra, cores)

        print(f"Tentativa {tentativa + 1}: {palavra} => {resultado}")

        if resultado == "🟩🟩🟩🟩🟩":
            print("Acertou!")
            break

jogar()
