import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects  # Добавляем импорт
import seaborn as sns
import subprocess
import sys
import os
import numpy as np
from matplotlib.ticker import ScalarFormatter
import pandas as pd

def compile_and_run_cpp():
    try:
        subprocess.run(['g++', 'main.cpp', '-o', 'main', '-std=c++11'], check=True)
        process = subprocess.Popen(['./main'], stdout=subprocess.PIPE, universal_newlines=True)
        return process
    except subprocess.CalledProcessError:
        print("Ошибка компиляции")
        sys.exit(1)

def process_data(process):
    data = {}
    for line in process.stdout:
        scale, N, S_approx, relative_error = line.strip().split()
        N = int(N)
        if N < 1000:
            continue
        S_approx = float(S_approx)
        relative_error = float(relative_error)
        if scale not in data:
            data[scale] = {'N': [], 'S_approx': [], 'relative_error': []}
        data[scale]['N'].append(N)
        data[scale]['S_approx'].append(S_approx)
        data[scale]['relative_error'].append(relative_error)
    return data

def create_dataframe(data):
    df_list = []
    for scale in data:
        for n, s_approx, rel_error in zip(data[scale]['N'], 
                                         data[scale]['S_approx'], 
                                         data[scale]['relative_error']):
            df_list.append({
                'Масштаб': scale,
                'N': n,
                'Площадь': s_approx,
                'Относительная ошибка': rel_error
            })
    df = pd.DataFrame(df_list)
    df['Область'] = df['Масштаб'].map({
        'tight': 'Точная область',
        'wide': 'Расширенная область'
    })
    return df

def setup_style():
    plt.style.use('seaborn-v0_8')
    custom_colors = ['#2E86C1', '#E74C3C']
    sns.set_palette(custom_colors)
    plt.rcParams.update({
        'figure.figsize': (12, 6),
        'figure.dpi': 100,
        'font.size': 12,
        'font.family': 'sans-serif',
        'axes.facecolor': 'white',
        'figure.facecolor': 'white',
        'grid.color': '#CCCCCC',
        'grid.linestyle': '--',
        'grid.alpha': 0.7,
        'text.color': '#2C3E50',
        'axes.labelcolor': '#2C3E50',
        'xtick.color': '#2C3E50',
        'ytick.color': '#2C3E50'
    })

def format_tick_labels(x, _):
    if x >= 1000:
        return f'{x/1000:.0f}k'
    return str(int(x))

def plot_area(df, ax):
    g = sns.lineplot(data=df, x='N', y='Площадь', hue='Область',
                     linewidth=2.5, marker='o', markersize=6, ax=ax)
    
    exact_area = 0.25 * np.pi + 1.25 * np.arcsin(0.8) - 1
    ax.axhline(y=exact_area, color='#27AE60', linestyle='--', alpha=0.8)
    
    g.xaxis.set_major_formatter(plt.FuncFormatter(format_tick_labels))
    g.set_title('Зависимость приближенной площади от количества точек',
                fontsize=16, pad=20, color='#2C3E50', weight='bold')
    g.set_xlabel('Количество точек (N × 1000)', fontsize=14, color='#2C3E50')
    g.set_ylabel('Приближенная площадь', fontsize=14, color='#2C3E50')
    
    for i, scale in enumerate(df['Масштаб'].unique()):
        last_point = df[df['Масштаб'] == scale].iloc[-1]
        y_offset = 10 if i % 2 == 0 else -15
        plt.annotate(
            f'{last_point["Площадь"]:.3f}',
            (last_point['N'], last_point['Площадь']),
            xytext=(10, y_offset),
            textcoords='offset points',
            color='#2C3E50',
            fontweight='bold'
        )
    return g

def plot_error(df, ax):
    g = sns.lineplot(data=df, x='N', y='Относительная ошибка', hue='Область',
                     linewidth=2.5, marker='o', markersize=6, ax=ax)
    
    g.xaxis.set_major_formatter(plt.FuncFormatter(format_tick_labels))
    g.set_title('Зависимость относительной ошибки от количества точек',
                fontsize=16, pad=20, color='#2C3E50', weight='bold')
    g.set_xlabel('Количество точек (N × 1000)', fontsize=14, color='#2C3E50')
    g.set_ylabel('Относительная ошибка', fontsize=14, color='#2C3E50')
    plt.yscale('log')
    
    for i, scale in enumerate(df['Масштаб'].unique()):
        last_point = df[df['Масштаб'] == scale].iloc[-1]
        y_offset = 10 if i % 2 == 0 else -15
        plt.annotate(
            f'{last_point["Относительная ошибка"]:.2e}',
            (last_point['N'], last_point['Относительная ошибка']),
            xytext=(10, y_offset),
            textcoords='offset points',
            color='#2C3E50',
            fontweight='bold'
        )
    return g

def main():
    process = compile_and_run_cpp()
    data = process_data(process)
    df = create_dataframe(data)
    setup_style()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    plot_area(df, ax1)
    plot_error(df, ax2)
    
    plt.tight_layout()
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/results.png', dpi=300, bbox_inches='tight')
    os.remove('./main')
    plt.show()

if __name__ == "__main__":
    main()
