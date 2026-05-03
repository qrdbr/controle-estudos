# Makefile para o projeto Controle de Estudos

.PHONY: install run test clean

# Instalar dependências
install:
	pip install -r requirements.txt

# Executar a API
run:
	python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Executar testes
test:
	pytest

# Limpar cache de Python (opcional)
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete