# Household Budget PWA v9 — widget-focus

Mudança principal:
- removidas as quatro caixas superiores:
  - Income
  - Household Burn
  - Work Reimbursable
  - Available

A tela principal agora fica focada em:
- Total Budget Progress
- Spending Targets
- actual / target
- percentual
- status visual por categoria

Esses quatro indicadores podem voltar depois em:
- dashboard desktop;
- tela detalhada do app;
- Widget Layout 2 / Summary.

## Atualizar no GitHub Pages

Substitua no repositório:
- `index.html`
- `sw.js`
- `manifest.webmanifest`

Depois faça Commit changes.

O `sw.js` usa cache `household-budget-pwa-v9`, então a nova versão deve substituir a anterior automaticamente após a propagação do GitHub Pages.
