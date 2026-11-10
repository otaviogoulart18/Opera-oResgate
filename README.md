# Operação Resgate Orbital 
Minijogo 3D interativo desenvolvido como Trabalho Prático de Computação Gráfica, utilizando Python, Pygame e PyOpenGL.

  Identificação
Instituição: IFSULDEMINAS – Campus Machado
Disciplina: Computação Gráfica
Professor:Renan
Aluno: Otávio Henrique de Paiva Goulart
Data de Entrega: 11/11/2026
Sobre o Projeto
O jogo simula uma missão espacial onde o jogador pilota um drone de manutenção em uma estação abandonada. O objetivo principal é explorar o ambiente tridimensional, desviar de obstáculos (caixas industriais), recolher cinco células de energia espalhadas pelo cenário e alcançar o portal de saída, que altera dinamicamente o seu estado visual assim que todos os itens são recolhidos.

O projeto foi inteiramente construído com código procedural e primitivas geométricas do OpenGL, implementando conceitos avançados da disciplina, tais como:
* Sistema de coordenadas tridimensionais com projeção em perspectiva e teste de profundidade (`GL_DEPTH_TEST`).
* Transformações geométricas (Translação, Rotação e Escala).
* Transformação hierárquica (corpo central, braços e hélices rotativas acopladas).
* Animações contínuas e periódicas independentes de *framerate* através do uso de Delta Time (`dt`).
* Mapeamento e repetição de texturas coordenadas em superfícies.
* Sistema de iluminação dinâmica com cálculo explícito de vetores normais (`glNormal3f`).
 Pré-requisitos e Instalação

Certifique-se de ter o **Python** instalado em sua máquina. Em seguida, abra o terminal na pasta do projeto e instale as dependências executando o seguinte comando:
bash
pip install pygame PyOpenGL Pillow numpy
