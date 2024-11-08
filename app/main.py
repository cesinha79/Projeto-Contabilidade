from flask import Flask, request, jsonify
from .database import get_db_connection
from .models import init_db

app = Flask(__name__)
init_db()

@app.route('/contas-contabeis/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_contas_contabeis():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if request.method == 'GET':
            cursor.execute("SELECT * FROM contas_contabeis")
            contas = cursor.fetchall()
            contas_list = [{"id": row[0], "nome": row[1], "descricao": row[2]} for row in contas]
            return jsonify(contas_list)

        elif request.method == 'POST':
            data = request.json
            cursor.execute("INSERT INTO contas_contabeis (nome, descricao) VALUES (?, ?)",
                           (data['nome'], data['descricao']))
            conn.commit()
            return jsonify({"message": "Conta contábil criada com sucesso"}), 201

        elif request.method == 'PUT':
            data = request.json
            cursor.execute("UPDATE contas_contabeis SET nome = ?, descricao = ? WHERE id = ?",
                           (data['nome'], data['descricao'], data['id']))
            conn.commit()
            return jsonify({"message": "Conta contábil atualizada com sucesso"})

        elif request.method == 'DELETE':
            conta_id = request.json['id']
            cursor.execute("DELETE FROM contas_contabeis WHERE id = ?", (conta_id,))
            conn.commit()
            return jsonify({"message": "Conta contábil excluída com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/centros-custo/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_centros_custo():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if request.method == 'GET':
            cursor.execute("SELECT * FROM centros_custo")
            centros = cursor.fetchall()
            centros_list = [{"id": row[0], "nome": row[1], "descricao": row[2]} for row in centros]
            return jsonify(centros_list)

        elif request.method == 'POST':
            data = request.json
            cursor.execute("INSERT INTO centros_custo (nome, descricao) VALUES (?, ?)",
                           (data['nome'], data['descricao']))
            conn.commit()
            return jsonify({"message": "Centro de custo criado com sucesso"}), 201

        elif request.method == 'PUT':
            data = request.json
            cursor.execute("UPDATE centros_custo SET nome = ?, descricao = ? WHERE id = ?",
                           (data['nome'], data['descricao'], data['id']))
            conn.commit()
            return jsonify({"message": "Centro de custo atualizado com sucesso"})

        elif request.method == 'DELETE':
            centro_id = request.json['id']
            cursor.execute("DELETE FROM centros_custo WHERE id = ?", (centro_id,))
            conn.commit()
            return jsonify({"message": "Centro de custo excluído com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/lancamentos/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_lancamentos():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if request.method == 'GET':
            cursor.execute("SELECT * FROM lancamentos")
            lancamentos = cursor.fetchall()
            lancamentos_list = [
                {
                    "id": row[0],
                    "conta_contabil_id": row[1],
                    "centro_custo_id": row[2],
                    "historico": row[3],
                    "tipo": row[4],
                    "valor": row[5],
                    "data": row[6]
                }
                for row in lancamentos
            ]
            return jsonify(lancamentos_list)

        elif request.method == 'POST':
            data = request.json
            cursor.execute(
                "INSERT INTO lancamentos (conta_contabil_id, centro_custo_id, historico, tipo, valor, data) VALUES (?, ?, ?, ?, ?, ?)",
                (data['conta_contabil_id'], data['centro_custo_id'], data['historico'], data['tipo'], data['valor'], data['data'])
            )
            conn.commit()
            return jsonify({"message": "Lançamento criado com sucesso"}), 201

        elif request.method == 'PUT':
            data = request.json
            cursor.execute(
                "UPDATE lancamentos SET conta_contabil_id = ?, centro_custo_id = ?, historico = ?, tipo = ?, valor = ?, data = ? WHERE id = ?",
                (data['conta_contabil_id'], data['centro_custo_id'], data['historico'], data['tipo'], data['valor'], data['data'], data['id'])
            )
            conn.commit()
            return jsonify({"message": "Lançamento atualizado com sucesso"})

        elif request.method == 'DELETE':
            lancamento_id = request.json['id']
            cursor.execute("DELETE FROM lancamentos WHERE id = ?", (lancamento_id,))
            conn.commit()
            return jsonify({"message": "Lançamento excluído com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
