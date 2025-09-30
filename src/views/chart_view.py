import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ClassificationChartWindow(tk.Toplevel):
    def __init__(self, parent, chart_data, geometry=None): 
        super().__init__(parent)
        self.title("Distribuição de Classificações")
        
        if geometry:
            self.geometry(geometry)
        else:
            self.geometry("600x600")

        self.transient(parent)

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.update_chart(chart_data)

    def update_chart(self, chart_data):
        
        self.fig.clear()

        if not chart_data:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, "Não há dados para exibir.", 
                    horizontalalignment='center', verticalalignment='center')
            ax.axis('off')
            self.canvas.draw()
            return
            
        labels = [item[0] for item in chart_data]
        sizes = [item[1] for item in chart_data]

        ax = self.fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
        ax.axis('equal')

        self.canvas.draw()