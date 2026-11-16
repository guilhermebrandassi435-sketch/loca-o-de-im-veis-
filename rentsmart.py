# -*- coding: utf-8 -*-
"""
RentSmart - Sistema de Orcamento de Locacao
Aluno: GUILHERME BRANDASSI
RA: 238342
Turma: Manha
Curso: Analise e Desenvolvimento de Sistemas (ADS)

Trabalho da disciplina: Algorithmic Thinking & Introduction to
Object-Oriented Programming - 2026

Programa que calcula o valor do aluguel de um imovel (apartamento,
casa ou estudio), soma os adicionais, aplica o desconto quando for o
caso, divide a taxa do contrato em parcelas, mostra o orcamento e
gera o arquivo projecao_12_meses.csv.
"""

import csv

# ---------------------------------------------------------------
# Constantes de valor (tabela do enunciado)
# ---------------------------------------------------------------
TAXA_CONTRATO = 2000.00
MAX_PARCELAS = 5

VALOR_BASE = {
    "apartamento": 700.00,
    "casa": 900.00,
    "estudio": 1200.00,
}

SEGUNDO_QUARTO = {
    "apartamento": 200.00,
    "casa": 250.00,
}

GARAGEM = {
    "apartamento": 300.00,
    "casa": 300.00,
}

ESTUDIO_PACOTE_VAGAS = 250.00   # pacote das duas primeiras vagas
ESTUDIO_VAGA_EXTRA = 60.00      # cada vaga a mais
DESCONTO_SEM_CRIANCAS = 0.05    # 5% para apartamento sem criancas

NOME_ARQUIVO_CSV = "projecao_12_meses.csv"
MESES_PROJECAO = 12


# ---------------------------------------------------------------
# Funcoes auxiliares de entrada
# ---------------------------------------------------------------
def perguntar_opcao(mensagem, opcoes):
    """Pergunta ao usuario ate que ele digite uma opcao valida."""
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in opcoes:
            return resposta
        print("Opcao invalida. Digite uma das opcoes: {}.".format(", ".join(opcoes)))


def perguntar_inteiro(mensagem, minimo=0, maximo=None):
    """Pergunta um numero inteiro dentro do intervalo permitido."""
    while True:
        resposta = input(mensagem).strip()
        if resposta.isdigit():
            valor = int(resposta)
            if valor >= minimo and (maximo is None or valor <= maximo):
                return valor
        if maximo is None:
            print("Valor invalido. Digite um numero inteiro maior ou igual a {}.".format(minimo))
        else:
            print("Valor invalido. Digite um numero inteiro entre {} e {}.".format(minimo, maximo))


def perguntar_sim_nao(mensagem):
    """Pergunta uma resposta de sim ou nao e devolve True/False."""
    return perguntar_opcao(mensagem, ["s", "n"]) == "s"


# ---------------------------------------------------------------
# Classe Imovel
# ---------------------------------------------------------------
class Imovel:
    """Guarda os dados de um imovel e calcula o valor do aluguel."""

    def __init__(self, tipo, quartos=1, garagem=False, vagas=0, sem_criancas=False):
        self.tipo = tipo
        self.quartos = quartos
        self.garagem = garagem
        self.vagas = vagas
        self.sem_criancas = sem_criancas

    def valor_base(self):
        return VALOR_BASE[self.tipo]

    def adicional_segundo_quarto(self):
        if self.tipo in SEGUNDO_QUARTO and self.quartos == 2:
            return SEGUNDO_QUARTO[self.tipo]
        return 0.0

    def adicional_garagem(self):
        if self.tipo in GARAGEM and self.garagem:
            return GARAGEM[self.tipo]
        return 0.0

    def adicional_vagas_estudio(self):
        """Primeiras duas vagas em pacote; cada vaga a mais custa 60."""
        if self.tipo != "estudio" or self.vagas == 0:
            return 0.0
        valor = ESTUDIO_PACOTE_VAGAS
        if self.vagas > 2:
            valor += (self.vagas - 2) * ESTUDIO_VAGA_EXTRA
        return valor

    def valor_desconto(self):
        """Desconto de 5% para apartamento sem criancas, apos os adicionais."""
        if self.tipo == "apartamento" and self.sem_criancas:
            return self.desconto_aplicado * 0
        return 0.0

    def valor_bruto(self):
        """Valor base mais todos os adicionais, antes do desconto."""
        return (self.valor_base()
                + self.adicional_segundo_quarto()
                + self.adicional_garagem()
                + self.adicional_vagas_estudio())

    def calcular_aluguel(self):
        """Valor final do aluguel, com o desconto aplicado."""
        bruto = self.valor_bruto()
        if self.tipo == "apartamento" and self.sem_criancas:
            return bruto * (1 - DESCONTO_SEM_CRIANCAS)
        return bruto

    def descricao(self):
        """Resumo dos dados do imovel em uma linha."""
        partes = [self.tipo.capitalize(), "{} quarto(s)".format(self.quartos)]
        if self.tipo == "estudio":
            partes.append("{} vaga(s)".format(self.vagas))
        else:
            partes.append("com garagem" if self.garagem else "sem garagem")
        if self.tipo == "apartamento":
            partes.append("sem criancas" if self.sem_criancas else "com criancas")
        return " - ".join(partes)


# ---------------------------------------------------------------
# Classe Orcamento
# ---------------------------------------------------------------
class Orcamento:
    """Recebe o imovel e as parcelas, mostra o resumo e gera o CSV."""

    def __init__(self, imovel, parcelas):
        self.imovel = imovel
        self.parcelas = parcelas
        self.aluguel = imovel.calcular_aluguel()
        self.valor_parcela_taxa = TAXA_CONTRATO / parcelas

    def taxa_do_mes(self, mes):
        """A taxa entra na projecao so nos meses do parcelamento."""
        if mes <= self.parcelas:
            return self.valor_parcela_taxa
        return 0.0

    def total_do_mes(self, mes):
        return self.aluguel + self.taxa_do_mes(mes)

    def projecao(self):
        """Lista de tuplas (mes, aluguel, taxa, total) para 12 meses."""
        linhas = []
        for mes in range(1, MESES_PROJECAO + 1):
            linhas.append((mes, self.aluguel, self.taxa_do_mes(mes), self.total_do_mes(mes)))
        return linhas

    def mostrar_resumo(self):
        print("\n" + "=" * 52)
        print("ORCAMENTO DE LOCACAO - RENTSMART".center(52))
        print("=" * 52)
        print("Imovel          : {}".format(self.imovel.descricao()))
        print("Valor base      : R$ {:,.2f}".format(self.imovel.valor_base()))
        print("Segundo quarto  : R$ {:,.2f}".format(self.imovel.adicional_segundo_quarto()))
        if self.imovel.tipo == "estudio":
            print("Vagas           : R$ {:,.2f}".format(self.imovel.adicional_vagas_estudio()))
        else:
            print("Garagem         : R$ {:,.2f}".format(self.imovel.adicional_garagem()))
        if self.imovel.tipo == "apartamento" and self.imovel.sem_criancas:
            desconto = self.imovel.valor_bruto() - self.aluguel
            print("Desconto (5%)   : -R$ {:,.2f}".format(desconto))
        print("-" * 52)
        print("ALUGUEL MENSAL  : R$ {:,.2f}".format(self.aluguel))
        print("Taxa do contrato: R$ {:,.2f} em {}x de R$ {:,.2f}".format(
            TAXA_CONTRATO, self.parcelas, self.valor_parcela_taxa))
        print("-" * 52)
        print("Previsao dos 12 primeiros meses:")
        print("{:>4}  {:>12}  {:>12}  {:>12}".format("Mes", "Aluguel", "Taxa", "Total"))
        for mes, aluguel, taxa, total in self.projecao():
            print("{:>4}  {:>12,.2f}  {:>12,.2f}  {:>12,.2f}".format(mes, aluguel, taxa, total))
        total_12 = sum(linha[3] for linha in self.projecao())
        print("-" * 52)
        print("TOTAL PREVISTO (12 meses): R$ {:,.2f}".format(total_12))
        print("=" * 52)

    def gerar_csv(self, nome_arquivo=NOME_ARQUIVO_CSV):
        """Cria o CSV com a previsao dos 12 meses."""
        with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mes", "Aluguel (R$)", "Taxa contratual (R$)", "Total previsto (R$)"])
            for mes, aluguel, taxa, total in self.projecao():
                escritor.writerow([mes, "{:.2f}".format(aluguel),
                                   "{:.2f}".format(taxa), "{:.2f}".format(total)])
        print("Arquivo '{}' criado com a previsao dos 12 meses.".format(nome_arquivo))
        return nome_arquivo


# ---------------------------------------------------------------
# Coleta dos dados da locacao
# ---------------------------------------------------------------
def coletar_imovel():
    """Pergunta os dados da locacao e devolve um objeto Imovel."""
    print("\nTipos de imovel disponiveis:")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estudio")

    escolha = perguntar_opcao("Escolha o tipo de imovel (1, 2 ou 3): ", ["1", "2", "3"])
    tipos = {"1": ("apartamento", "Apartamento"),
             "2": ("casa", "Casa"),
             "3": ("estudio", "Estudio")}
    tipo, nome = tipos[escolha]
    print("Tipo escolhido: {}".format(nome))

    if tipo == "estudio":
        vagas = perguntar_inteiro("Quantas vagas de garagem? (0 a 10): ", 0, 10)
        return Imovel(tipo, quartos=1, vagas=vagas)

    quartos = perguntar_inteiro("Quantos quartos? (1 ou 2): ", 1, 2)
    garagem = perguntar_sim_nao("Possui vaga de garagem? (s/n): ")
    sem_criancas = False
    if tipo == "apartamento":
        sem_criancas = perguntar_sim_nao("O cliente nao possui criancas? (s/n): ")
    return Imovel(tipo, quartos=quartos, garagem=garagem, sem_criancas=sem_criancas)


def coletar_parcelas():
    """Pergunta em quantas vezes a taxa do contrato sera paga."""
    return perguntar_inteiro(
        "Em quantas vezes deseja pagar a taxa do contrato? (1 a {}): ".format(MAX_PARCELAS),
        1, MAX_PARCELAS)


# ---------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------
def main():
    print("=" * 52)
    print(" RENTSMART - SISTEMA DE ORCAMENTO DE LOCACAO ".center(52, "="))
    print("=" * 52)
    print("Informe os dados da locacao.\n")

    imovel = coletar_imovel()
    parcelas = coletar_parcelas()

    orcamento = Orcamento(imovel, parcelas)
    orcamento.mostrar_resumo()
    orcamento.gerar_csv()

    print("\nObrigado por usar o RentSmart!")


if __name__ == "__main__":
    main()
