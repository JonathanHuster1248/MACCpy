from plotnine import *
import constants

def plot_MACC(df, title = "Power Plant MACC", x_lab = "tonnes of CO2", y_lab = "$/tonne CO2", x_min = None, x_max = None, y_min = None, y_max = None, save = True, file = "MACC_plot.png"):
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
    
    if x_min or x_max:
        fig = fig + xlim(x_min,x_max)
    if y_min or y_max:
        fig = fig + ylim(y_min,y_max)

    if save:
        fig.save(file, dpi=600)
    
    return fig


def highlight_state(df, state, title = "Power Plant MACC", x_lab = "tonnes of CO2", y_lab = "$/tonne CO2", save = True, file = "MACC_plot.png"):
    state_data = df[df.state == state]
    other_data = df[df.state != state]
    other_data.loc[:, "ori_rep"] = "National"
    fig = (
      ggplot() +
        aes(xmin = "cum_red_prev", 
            xmax = "cum_red",
            ymin = 0, 
            ymax = "metric",
            fill = "ori_rep")+
        geom_rect(data = other_data, alpha = 0.4) +
        geom_rect(data = state_data) +
        # geom_label(aes(x = lab_xloc, y = lab_yloc, label = round(lab_val, 3)), size = 5)+
         labs(
            x=x_lab,
            y=y_lab,
            fill="Fuel Switch",
            title=title)
        + scale_fill_manual(values = constants.colors)
        # + scale_alpha_manual(values = constants.alphas, labels = 'none')
        # ylim(-200,200)+
        # xlim(0,1.2)
    ) 

    if save:
        fig.save(file, dpi=600)
    
    return fig

