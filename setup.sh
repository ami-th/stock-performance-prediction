mkdir -p ~/.streamlit/
echo "
[general]n
email = "amithchndran@gmail.com"
" > ~/.streamlit/credentials.toml
echo "
[server]n
headless = truen
enableCORS=falsen
port = $PORTn
" > ~/.streamlit/config.toml