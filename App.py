import pandas as pd
import unicodedata
import os


# ===== 1. FUNÇÃO PARA NORMALIZAR TEXTOS =====
def remover_acentos(texto):
    if isinstance(texto, str):
        return unicodedata.normalize('NFKD', texto).encode('ascii', errors='ignore').decode('utf-8').strip().lower()
    return texto

# ===== 2. CARREGAR E NORMALIZAR O CSV =====
df = pd.read_csv('autopecas.csv', dtype=str)

# ===== 3. FUNÇÕES DE BUSCA =====
def buscar_categorias(tipo_veiculo):
    categorias = df[df['tipo_de_veiculo'] == tipo_veiculo]['categoria_das_pecas'].dropna().unique().tolist()
    return sorted(categorias)

def buscar_pecas_por_categoria(categoria, tipo_veiculo):
    return sorted(df[(df['categoria_das_pecas'] == categoria) & 
                     (df['tipo_de_veiculo'] == tipo_veiculo)]['nome_das_pecas'].dropna().unique().tolist())

def buscar_marcas_por_produto(produto, tipo_veiculo):
    return sorted(df[(df['nome_das_pecas'] == produto) & 
                     (df['tipo_de_veiculo'] == tipo_veiculo)]['marca_das_pecas'].dropna().unique().tolist())

def buscar_modelos_por_marca(produto, marca, tipo_veiculo):
    return sorted(df[(df['nome_das_pecas'] == produto) & 
                     (df['marca_das_pecas'] == marca) & 
                     (df['tipo_de_veiculo'] == tipo_veiculo)]['modelo_do_veiculo_compativel'].dropna().unique().tolist())

# ===== 4. MENU INTERATIVO =====
def menu():
    while True:
        print("\n=== MENU ===")
        print("1. Buscar Peças")
        print("2. Sair do App")
        
        escolha = input("Digite sua opção (1-2): ").strip()
        
        if escolha == '1':
            print("\nEscolha o tipo de veículo:")
            print("1. Carro")
            print("2. Caminhão")
            
            tipo_opcao = input("Digite sua opção (1-2): ").strip()
            tipo_veiculo = 'carro' if tipo_opcao == '1' else 'caminhao' if tipo_opcao == '2' else None
            
            if not tipo_veiculo:
                input("Opção inválida. Pressione Enter para continuar...")
                continue
            
            categorias = buscar_categorias(tipo_veiculo)
            if not categorias:
                input("Nenhuma categoria encontrada. Pressione Enter para continuar...")
                continue

            print("\nCategorias disponíveis:")
            for i, categoria in enumerate(categorias, 1):
                print(f"{i}. {categoria}")
            
            categoria_escolhida = input("\nEscolha uma categoria pelo número: ").strip()
            if not categoria_escolhida.isdigit() or int(categoria_escolhida) not in range(1, len(categorias) + 1):
                input("Opção inválida. Pressione Enter para voltar ao menu...")
                continue
            categoria_nome = categorias[int(categoria_escolhida) - 1]

            pecas = buscar_pecas_por_categoria(categoria_nome, tipo_veiculo)
            print(f"\nPeças disponíveis para {categoria_nome}:")
            for i, peca in enumerate(pecas, 1):
                print(f"{i}. {peca}")
            
            peca_escolhida = input("\nEscolha uma peça pelo número: ").strip()
            if not peca_escolhida.isdigit() or int(peca_escolhida) not in range(1, len(pecas) + 1):
                input("Opção inválida. Pressione Enter para voltar ao menu...")
                continue
            peca_nome = pecas[int(peca_escolhida) - 1]

            marcas = buscar_marcas_por_produto(peca_nome, tipo_veiculo)
            print("\nMarcas disponíveis:")
            for i, marca in enumerate(marcas, 1):
                print(f"{i}. {marca}")

            marca_escolhida = input("\nEscolha uma marca pelo número: ").strip()
            if not marca_escolhida.isdigit() or int(marca_escolhida) not in range(1, len(marcas) + 1):
                input("Opção inválida. Pressione Enter para voltar ao menu...")
                continue
            marca_nome = marcas[int(marca_escolhida) - 1]

            modelos = buscar_modelos_por_marca(peca_nome, marca_nome, tipo_veiculo)
            print("\nModelos disponíveis:")
            for i, modelo in enumerate(modelos, 1):
                print(f"{i}. {modelo}")

            modelo_escolhido = input("\nEscolha um modelo pelo número: ").strip()
            if not modelo_escolhido.isdigit() or int(modelo_escolhido) not in range(1, len(modelos) + 1):
                input("Opção inválida. Pressione Enter para voltar ao menu...")
                continue
            modelo_nome = modelos[int(modelo_escolhido) - 1]

            filtro = (
                (df['categoria_das_pecas'] == categoria_nome) &
                (df['tipo_de_veiculo'] == tipo_veiculo) &
                (df['nome_das_pecas'] == peca_nome) &
                (df['marca_das_pecas'] == marca_nome) &
                (df['modelo_do_veiculo_compativel'] == modelo_nome)
            )

            pecas_encontradas = df[filtro]
            if pecas_encontradas.empty:
                print("❌ Nenhum detalhe encontrado para essa combinação.")
            else:
                print(f"🔧 {len(pecas_encontradas)} peça(s) encontrada(s):\n")
                for i, peca in pecas_encontradas.iterrows():
                    print("📦 Detalhes da Peça Selecionada:")
                    print(f"📌 Nome:           {peca['nome_das_pecas'].title()}")
                    print(f"🏷️  Marca:          {peca['marca_das_pecas'].title()}")
                    print(f"🚗 Modelo:         {peca['modelo_do_veiculo_compativel'].title()}")
                    print(f"📅 Ano:            {peca['ano_do_veiculo_compativel']}")
                    print(f"💰 Preço:          R$ {peca['preco_da_peca']}")
                    print(f"📦 Estoque:        {peca['estoque']}")
                    print(f"🏭 Fornecedor:     {peca['fornecedor_da_peca'].title()}")
                    print(f"⚖️  Peso:           {peca['peso_da_peca_(kg)']} kg")
                    print(f"📐 Dimensões:      {peca['dimensao_da_peca_(cm)']} cm")
                    print(f"🔩 Material:       {peca['material_principal_da_peca'].title()}")
                    print(f"🛡️  Garantia:       {peca['garantia_(meses)']} meses")
                    print(f"🌍 Origem:         {peca['origem_da_peca'].title()}")
                    print(f"🧾 Número OEM:     {peca['numero_oem']}")
                    print(f"📝 Descrição:      {peca['descricao_da_peca'].capitalize()}")
                    print("-" * 60 + "\n")

        elif escolha == '2':
            print("Saindo do aplicativo. Até logo!")
            break
        else:
            input("Opção inválida. Pressione Enter para tentar novamente...")

# ===== 5. EXECUTAR =====
menu()
