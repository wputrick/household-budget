# Household Budget PWA v7 — ready for iPhone/iPad test

Esta versão foi preparada especificamente porque você não tem Mac.

Ela permite validar agora:
- layout no iPhone/iPad;
- instalação na Home Screen;
- modo standalone;
- barras de progresso;
- categorias;
- total budget progress;
- mini gráfico de tendência;
- leitura confortável em widget-like full app.

## O que NÃO é ainda
Esta PWA não é um WidgetKit nativo. O iOS não permite criar um widget nativo real sem compilar um app iOS em macOS/Xcode.

Para o primeiro teste, isso não importa: o objetivo é aprovar visual, organização, quantidade de informações e navegação.

## Como publicar sem Mac

A pasta é totalmente estática.

Opções simples:
- Netlify Drop
- Cloudflare Pages
- GitHub Pages
- Vercel static

A forma mais simples costuma ser Netlify Drop:
1. descompacte o ZIP;
2. abra o serviço de deploy pelo navegador no iPad/PC;
3. envie a pasta inteira;
4. aguarde a URL HTTPS.

## Instalar no iPhone/iPad

1. Abra a URL HTTPS no Safari.
2. Toque em Share.
3. Escolha **Add to Home Screen**.
4. Confirme.
5. Abra pelo novo ícone.

O app abrirá sem a barra normal do Safari, em modo standalone.

## O que testar

- leitura rápida dos 4 números superiores;
- se o Total Budget Progress é útil;
- se 5 categorias é demais ou de menos;
- se as barras estão fáceis de interpretar;
- se o mini gráfico agrega valor;
- se você prefere mais categorias ou mais espaço por categoria;
- se prefere porcentagem, valor, ou ambos;
- se o visual escuro funciona bem no uso diário.

## Depois da aprovação

1. publicar backend real;
2. ativar modo Live;
3. ligar bancos/cartões;
4. sincronizar reimbursements;
5. usar Mac na nuvem/CI para compilar o app iOS;
6. distribuir via TestFlight;
7. instalar WidgetKit nativo.
