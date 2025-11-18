# Space exploders

Este é um jogo de plataforma 2D simples desenvolvido com a biblioteca Pygame Zero em Python. O jogador controla um herói que deve navegar por fases geradas aleatoriamente, pulando em plataformas e derrotando inimigos.

## Funcionalidades

-   **Geração Aleatória de Fases:** As plataformas são geradas de forma aleatória a cada vez que uma nova partida começa, garantindo que cada jogada seja única.
-   **Combate por Contato:** Derrote os slimes simplesmente tocando neles.
-   **Inimigos Variados:** Enfrente diferentes tipos de slimes (normal, fogo, espinhos).
-   **Sistema de Som Completo:** O jogo conta com música de fundo para o menu e para as fases, além de efeitos sonoros para pulo, ataque, dano e interações de menu. É possível ligar ou desligar o som.

## Como Jogar

O objetivo é derrotar todos os inimigos da fase, tocando neles e evitando cair das plataformas.

### Controles

-   **Setas Esquerda/Direita:** Mover o personagem.
-   **Barra de Espaço:** Pular.
-   **Mouse:** Navegar e clicar nos botões do menu.
-   **Enter (na tela de Game Over):** Retornar ao menu principal.

## Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o Python e o Pygame Zero instalados. Se não tiver o Pygame Zero, você pode instalá-lo via pip:

```bash
pip install pgzero
```

### Executando o Jogo

1.  Navegue até o diretório raiz do projeto pelo terminal.
2.  Execute o seguinte comando:

```bash
python main.py
```

## Estrutura de Arquivos

**Importante:** Para que o Pygame Zero encontre os recursos (imagens, sons, fontes) corretamente, a estrutura de pastas deve ser a seguinte:

```
.
├── fonts/            # (Opcional) Fontes personalizadas (arquivos .ttf ou .otf)
├── images/           # Pasta principal para TODOS os recursos visuais
│   ├── backgrounds/  # Imagens de fundo para as fases
│   ├── effects/      # Animações de efeitos (ex: projectile_explosion_1.png, ...)
│   ├── enemy/        # Sprites e animações dos inimigos
│   ├── hero/         # Sprites e animações do personagem
│   └── tiles/        # Sprites para a geração das plataformas
├── sounds/           # Arquivos de áudio (músicas e efeitos sonoros)
├── main.py           # Lógica principal do jogo
├── player.py         # Classe do jogador
├── enemy.py          # Classe do inimigo
└── effects.py        # Classes de efeitos visuais (ex: animação de explosão)
```

## Bibliotecas Utilizadas

-   `pgzero`
-   `random`
