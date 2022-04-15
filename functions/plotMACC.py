from plotnine import *
import constants

def plotMACC(df, title = "Power Plant MACC", x_lab = "tonnes of CO2", y_lab = "$/tonne CO2", save = True, file = "MACC_plot.png"):
    fig = (
      ggplot(df) +
        aes(xmin = "cum_red_prev", 
            xmax = "cum_red",
            ymin = 0, 
            ymax = "metric",
            fill = "ori_rep")+
        geom_rect()+
        # geom_label(aes(x = lab_xloc, y = lab_yloc, label = round(lab_val, 3)), size = 5)+
         labs(
            x=x_lab,
            y=y_lab,
            fill="Fuel Switch",
            title=title)
        + scale_fill_manual(values = constants.colors)
        # ylim(-200,200)+
        # xlim(0,1.2)
    ) 

    if save:
        fig.save(file, dpi=600)
    
    return fig