from flask import render_template, request, jsonify, send_from_directory
from .database import get_db_connection, init_db
import sqlite3
import os

def configure_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/contas-contabeis/", methods=["GET", "POST"])
    def contas_contabeis():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if request.method == "POST":
                data = request.json
                cursor.execute("INSERT INTO contas_contabeis (nome, descricao) VALUES (?, ?)",
                               (data["nome"], data["descricao"]))
                conn.commit()
                return jsonify({"message": "Conta contábil criada com sucesso."}), 201

            elif request.method == "GET":
                # Renderiza o template HTML
                return render_template("contas.html")
        finally:
            conn.close()

    @app.route("/centros-custo/", methods=["GET", "POST"])
    def centros_custo():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if request.method == "POST":
                data = request.json
                cursor.execute("INSERT INTO centros_custo (nome, descricao) VALUES (?, ?)",
                               (data["nome"], data["descricao"]))
                conn.commit()
                return jsonify({"message": "Centro de custo criado com sucesso."}), 201

            elif request.method == "GET":
                # Renderiza o template HTML
                return render_template("centros.html")
        finally:
            conn.close()

    @app.route("/lancamentos/", methods=["GET", "POST"])
    def lancamentos():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if request.method == "POST":
                data = request.json

                # Verificação básica dos dados recebidos
                if not all(k in data for k in
                           ("conta_contabil_id", "centro_custo_id", "historico", "tipo", "valor", "data")):
                    return jsonify({"error": "Faltam campos obrigatórios"}), 400

                # Insere os dados na tabela lancamentos
                cursor.execute(
                    "INSERT INTO lancamentos (conta_contabil_id, centro_custo_id, historico, tipo, valor, "
                    "data) VALUES (?, ?, ?, ?, ?, ?)",
                    (data["conta_contabil_id"], data["centro_custo_id"], data["historico"], data["tipo"], data["valor"],
                     data["data"])
                )
                conn.commit()
                return jsonify({"message": "Lançamento contábil criado com sucesso."}), 201

            elif request.method == "GET":
                # Renderiza o template HTML para listagem de lançamentos
                return render_template("lancamentos.html")

        except sqlite3.Error as e:
            # Log de erro para depuração
            print("Erro no banco de dados:", e)
            return jsonify({"error": "Ocorreu um erro no banco de dados."}), 500

        finally:
            conn.close()

    @app.route('/marcar-duplicado/<int:id>/<string:table>/', methods=['POST'])
    def marcar_duplicado(id, table):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table} SET is_duplicate = 1 WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Registro {id} marcado como duplicado em {table}."})

    @app.route('/excluir-logicamente/<int:id>/<string:table>/', methods=['POST'])
    def excluir_logicamente(id, table):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table} SET is_deleted = 1 WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Registro {id} excluído logicamente de {table}."})

    @app.route('/gerar-relatorio', methods=['GET'])
    def gerar_relatorio():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM contas_contabeis WHERE is_duplicate = 1 OR is_deleted = 1")
        total_contas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM centros_custo WHERE is_duplicate = 1 OR is_deleted = 1")
        total_centros = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM lancamentos WHERE is_duplicate = 1 OR is_deleted = 1")
        total_lancamentos = cursor.fetchone()[0]

        conn.close()

        report = f"Contas Contábeis: {total_contas} duplicadas ou excluídas\n"
        report += f"Centros de Custo: {total_centros} duplicadas ou excluídas\n"
        report += f"Lançamentos: {total_lancamentos} duplicados ou excluídos\n"

        # Salva o relatório em um arquivo de texto
        report_path = os.path.join("app", "static", "relatorio_contabil.txt")
        with open(report_path, "w") as f:
            f.write(report)

        return jsonify({"message": "Relatório gerado com sucesso.", "download_link": "/static/relatorio_contabil.txt"})

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory('static', filename)
