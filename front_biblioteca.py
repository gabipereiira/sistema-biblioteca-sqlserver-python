import streamlit as st
import requests

# Configuração da URL
URL_API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Gerenciador de Biblioteca", page_icon="📚")
st.title("Gerenciador de Livros")
st.markdown("---")

# --- 1. SEÇÃO PARA ADICIONAR LIVRO ---
st.subheader("➕ Adicionar Novo Livro")
with st.container():
    # Linha 1: Campos Obrigatórios
    col1, col2 = st.columns(2)
    with col1:
        nome_novo = st.text_input("Nome do Livro (Obrigatório)", placeholder="Ex: O Alquimista")
    with col2:
        autor_novo = st.text_input("Autor (Obrigatório)", placeholder="Ex: Paulo Coelho")

    # Linha 2: Campos Opcionais
    col3, col4, col5 = st.columns([1, 2, 1])
    with col3:
        # Usamos 0 como valor padrão para indicar 'vazio'
        ano_novo = st.number_input("Ano (Opcional)", min_value=0, max_value=2026, value=0)
    with col4:
        editora_nova = st.text_input("Editora (Opcional)", placeholder="Ex: Rocco")
    with col5:
        paginas_novas = st.number_input("Páginas (Opcional)", min_value=0, value=0)

    if st.button("Cadastrar Livro", use_container_width=True):
        if nome_novo and autor_novo:
            # Montando o payload tratando os opcionais
            payload = {
                "nome": nome_novo,
                "autor": autor_novo,
                "ano": int(ano_novo) if ano_novo > 0 else None,
                "editora": editora_nova if editora_nova else None,
                "paginas": int(paginas_novas) if paginas_novas > 0 else None
            }

            try:
                response = requests.post(f"{URL_API}/adicionar-livro", json=payload)
                if response.status_code == 201:
                    st.success(f"Livro '{nome_novo}' cadastrado com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"Erro na API: {response.status_code}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
        else:
            st.warning("Por favor, preencha os campos obrigatórios (Nome e Autor).")

st.markdown("---")

# --- 2. SEÇÃO DE LISTAGEM ---
st.subheader("📚 Estante de Livros")

# 1. Criamos a "memória" para saber QUAL livro está sendo editado
if "id_editando" not in st.session_state:
    st.session_state.id_editando = None

try:
    response = requests.get(f"{URL_API}/mostrar-biblioteca")
    if response.status_code == 200:
        livros = response.json()

        if not livros:
            st.info("A biblioteca está vazia.")
        else:
            for livro in livros:
                # Criamos as colunas: Informação (4), Botão Editar (0.5), Botão Excluir (0.5)
                col_info, col_edit, col_del = st.columns([4, 0.5, 0.5])

                with col_info:
                    # PERGUNTA: "Este livro é o que eu cliquei para editar?"
                    if st.session_state.id_editando == livro['id']:
                        # --- MODO EDIÇÃO ---
                        st.write(f"🔧 **Editando ID: {livro['id']}**")
                        novo_nome = st.text_input("Novo nome", value=livro['nome'], key=f"n_{livro['id']}")
                        novo_autor = st.text_input("Novo autor", value=livro['autor'], key=f"a_{livro['id']}")

                        # Botões para Salvar ou Cancelar
                        c1, c2 = st.columns(2)
                        if c1.button("Salvar ✅", key=f"s_{livro['id']}"):
                            dados = {"nome": novo_nome, "autor": novo_autor}
                            # Envia para a API (Update)
                            requests.put(f"{URL_API}/atualizar-livro/{livro['id']}", json=dados)
                            st.session_state.id_editando = None  # Sai do modo edição
                            st.rerun()

                        if c2.button("Cancelar ❌", key=f"c_{livro['id']}"):
                            st.session_state.id_editando = None
                            st.rerun()
                    else:
                        # --- MODO LEITURA (O que você já tinha) ---
                        st.markdown(f"📖 **{livro['nome']}**")
                        st.caption(f"✍️ {livro['autor']}")

                with col_edit:
                    # Botão de Lápis: Liga o modo de edição para este ID
                    if st.button("📝", key=f"ed_btn_{livro['id']}"):
                        st.session_state.id_editando = livro['id']
                        st.rerun()

                with col_del:
                    # Botão de Lixeira: Deleta o livro
                    if st.button("🗑️", key=f"del_btn_{livro['id']}"):
                        requests.delete(f"{URL_API}/deletar-livro/{livro['id']}")
                        st.rerun()

                st.divider()  # Linha fina entre os livros para organizar o visual

except Exception as e:
    st.error(f"Erro ao carregar lista: {e}")

