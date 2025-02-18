FROM grosinosky/bigdata_fila3_jupyter

USER root

# Installer redis-cli
RUN apt-get update && apt-get install -y redis-tools

# Copier les fichiers
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copier le script d'import et le rendre exécutable
COPY src/data/import_data.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/import_data.sh

# Copier les fichiers source
COPY src/ /home/jovyan/work/

# Ajouter le chemin du module à PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/home/jovyan/work"

# Changer les permissions
RUN chown -R jovyan:users /home/jovyan/work

USER jovyan