import copy
import matplotlib.dates as mdates
import matplotlib.colors as colors
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def plot_radar_CFAD(Ze_EDGES, newgrid_mid, cfaddbz35_cal_alltime, save_flag, fig_path, fig_name):
    """
    generate radar CFAD figure

    Parameters
    ----------
    Ze_EDGES: float
        radar CFAD bins, unit: dBZ
    newgrid_mid: float
        height, unit: km
    cfaddbz35_cal_alltime: float
        radar cfad, unit: none
    save_flag: float
        0 or 1, if save (1) the figure or not (0)
    fig_path: string
        output figure directory
    fig_name: string
        output figure name
    """

    # height
    levStat_km = copy.deepcopy(newgrid_mid)
    levStat_km_add0 = np.arange(len(levStat_km) + 1) * 0.48

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 8))
    clb_dy, clb_ddy = 0.15, 0.03

    cdict = {'red': ((0., 1, 1),
                     (0.05, 1, 1),
                     (0.11, 0, 0),
                     (0.66, 1, 1),
                     (0.89, 1, 1),
                     (1, 0.5, 0.5)),
             'green': ((0., 1, 1),
                       (0.05, 1, 1),
                       (0.11, 0, 0),
                       (0.375, 1, 1),
                       (0.64, 1, 1),
                       (0.91, 0, 0),
                       (1, 0, 0)),
             'blue': ((0., 1, 1),
                      (0.05, 1, 1),
                      (0.11, 1, 1),
                      (0.34, 1, 1),
                      (0.65, 0, 0),
                      (1, 0, 0))}

    palette = matplotlib.colors.LinearSegmentedColormap(
        'my_colormap', cdict, 256)

    c1 = ax.pcolormesh(Ze_EDGES, levStat_km_add0,
                       cfaddbz35_cal_alltime, cmap=palette, vmin=0.0, vmax=0.2)
    ax.set_xlabel('Ze bins [dBZ]')
    ax.set_ylabel('Height [km]')
    ax.set_title('Radar')
    x1 = np.array(ax.get_position())[0, 0]
    y1 = np.array(ax.get_position())[0, 1]
    ddx = np.array(ax.get_position())[1, 0]-np.array(ax.get_position())[0, 0]
    cb_ax = fig.add_axes([x1, y1-clb_dy, ddx, clb_ddy])
    clb = fig.colorbar(c1, cax=cb_ax, orientation='horizontal')
    clb.set_label('frequency')
    ax.set_xlim(-50, 10)
    ax.set_xticks(np.arange(7)*10-50)
    ax.set_ylim(0, 15)

    if save_flag == 'save':
        fig.savefig(f'{fig_path}/CFAD_Radar_{fig_name}.png', dpi=400)


def plot_lidar_SR_CFAD(SR_EDGES, newgrid_mid, cfadSR_cal_alltime, save_flag, fig_path, fig_name):
    """
    Generate lidar CFAD figure

    Parameters
    ----------
    SR_EDGES: float
        lidar SR CFAD bins, unit: none
    newgrid_mid: float
        height, unit: km
    cfadSR_cal_alltime: float
        lidar SR cfad, unit: none
    save_flag: float
        0 or 1, if save (1) the figure or not (0)
    fig_path: string
        output figure directory
    fig_name: string
        output figure name

    """

    # height
    levStat_km = copy.deepcopy(newgrid_mid)
    levStat_km_add0 = np.arange(len(levStat_km) + 1) * 0.48

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 8))
    clb_dy, clb_ddy = 0.15, 0.03

    cdict = {'red': ((0., 1, 1),
                     (0.05, 1, 1),
                     (0.11, 0, 0),
                     (0.66, 1, 1),
                     (0.89, 1, 1),
                     (1, 0.5, 0.5)),
             'green': ((0., 1, 1),
                       (0.05, 1, 1),
                       (0.11, 0, 0),
                       (0.375, 1, 1),
                       (0.64, 1, 1),
                       (0.91, 0, 0),
                       (1, 0, 0)),
             'blue': ((0., 1, 1),
                      (0.05, 1, 1),
                      (0.11, 1, 1),
                      (0.34, 1, 1),
                      (0.65, 0, 0),
                      (1, 0, 0))}

    palette = matplotlib.colors.LinearSegmentedColormap(
        'my_colormap', cdict, 256)

    SR_BINS_index = np.arange(len(SR_EDGES))

    c1 = ax.pcolormesh(SR_BINS_index, levStat_km_add0,
                       cfadSR_cal_alltime, cmap=palette, vmin=0.0, vmax=0.2)
    ax.set_xlabel('SR bins')
    ax.set_ylabel('Height [km]')
    ax.set_title('Lidar')

    x1 = np.array(ax.get_position())[0, 0]
    y1 = np.array(ax.get_position())[0, 1]
    ddx = np.array(ax.get_position())[1, 0] - np.array(ax.get_position())[0, 0]
    cb_ax = fig.add_axes([x1, y1-clb_dy, ddx, clb_ddy])
    clb = fig.colorbar(c1, cax=cb_ax, orientation='horizontal')
    clb.set_label('frequency')
    ax.set_ylim(0, 15)
    ax.set_xticks(np.arange(8) * 2)
    labels = np.array([0., 1.2, 5.0, 10.0, 20.0, 30.0, 50.0, 80.0])
    ax.set_xticklabels(labels)

    if save_flag == 'save':
        fig.savefig(f'{fig_path}/CFAD_SR_{fig_name}.png', dpi=400)

# plot radar lidar signal with all subcolumns


def plot_every_subcolumn_timeseries_radarlidarsignal(
        model, col_index, save_flag, fig_path, fig_name):
    """
    generate timeseries of radar and lidar signal from every subcolumn.

    Parameters
    ----------
    model: func:`emc2.core.Model` class
        The model to read in some of pre-calculated variables.
    col_index: int
        column index, unit: none
    save_flag: float
        0 or 1, if save (1) the figure or not (0)
    fig_path: string
        output figure directory
    fig_name: string
        output figure name
    """

    subcolumn_num = len(model.ds.subcolumn)
    lev_num = len(model.ds.lev)
    x_variable = model.time_dim
    x_time = model.ds[x_variable].values
    loc_ground = np.arange(len(x_time)) + 1
    xval = np.hstack(
        ([i * loc_ground[-1] + loc_ground for i in range(subcolumn_num)]))
    x_date2num = mdates.date2num([y for y in x_time])
    f = interpolate.interp1d(loc_ground, x_date2num, fill_value="extrapolate")
    xnew = xval/subcolumn_num
    input_time_long = f(xnew)
    input_time_2d_long = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        input_time_2d_long[j, :] = input_time_long

    y_variable = model.z_field
    y_height = model.ds[y_variable].values / 1000.  # km
    input_height_half = y_height[:, :, col_index]
    input_height_half_long = np.empty((lev_num, len(xval)))
    xval_2d = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        xval_2d[j, :] = xval / subcolumn_num
        for i in np.arange(len(x_time)):
            input_height_half_long[
                j, subcolumn_num * (i):subcolumn_num*(i+1) + 1] = input_height_half[i, j]

    Ze_att_tot = model.ds['sub_col_Ze_att_tot'][:, :, :, col_index].values
    beta_att_tot = model.ds['sub_col_beta_att_tot'][:,
                                                    :, :, col_index].values

    Ze_att_tot_plt = np.transpose(
        Ze_att_tot, axes=(2, 1, 0)).reshape(lev_num, -1)
    beta_att_tot_plt = np.transpose(
        beta_att_tot, axes=(2, 1, 0)).reshape(lev_num, -1)

    x_dateformat = "%b%d-%H"
    x_rotation = 30

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(24*0.5, 12))
    fig.subplots_adjust(top=0.96, bottom=0.06, left=0.09,
                        right=0.9, wspace=0.1, hspace=0.2)
    ax = axes.flatten()
    cmap_plot = 'act_HomeyerRainbow'

    fontsize_input = 12
    plt.rcParams.update({'font.size': 12})

    textx, texty = 0.04, 1.03
    ifig = 0
    # var=np.transpose(dbze35_ground_th, axes=(0,2,1)).reshape(lev_ground.shape[0], -1)
    Ze_att_tot_plt[Ze_att_tot_plt <= -1.e+20] = np.nan
    c1 = ax[ifig].pcolormesh(input_time_2d_long, input_height_half_long,
                             Ze_att_tot_plt, vmin=-50, vmax=10, cmap=cmap_plot)
    ax[ifig].text(textx, texty, 'Radar', transform=ax[ifig].transAxes)
    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$Z_{e}$ [dBZ]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height [km]', fontsize=fontsize_input)

    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    vmin = 1e-8
    vmax = 1e-3

    ifig = 1
    # var=np.transpose(dbze35_ground_th, axes=(0,2,1)).reshape(lev_ground.shape[0], -1)
    beta_att_tot_plt[beta_att_tot_plt <= -1.e+40] = np.nan
    c1 = ax[ifig].pcolormesh(input_time_2d_long, input_height_half_long,
                             beta_att_tot_plt, norm=colors.LogNorm(vmin=vmin, vmax=vmax), cmap=cmap_plot)
    ax[ifig].text(textx, texty, 'Lidar', transform=ax[ifig].transAxes)
    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$\beta$ [$m^{-1} sr^{-1}$]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height [km]', fontsize=fontsize_input)
    ax[ifig].set_xlabel('Time [UTC]', fontsize=fontsize_input)
    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    if save_flag == 'save':
        fig.savefig(
            f'{fig_path}/radar_lidar_att_allsubcols_{fig_name}.png', dpi=400)


def plot_every_subcolumn_timeseries_nonatt_radarlidarsignal(model, col_index, save_flag, fig_path, fig_name):
    """
    Generate timeseries of non-attenuated radar and lidar signal from every subcolumn.

    Parameters
    ----------
    model: func:`emc2.core.Model` class
        The model to read in some of pre-calculated variables.
    col_index: int
        column index, unit: none
    save_flag: float
        0 or 1, if save (1) the figure or not (0)
    fig_path: string
        output figure directory
    fig_name: string
        output figure name

    """

    subcolumn_num = len(model.ds.subcolumn)
    lev_num = len(model.ds.lev)

    x_variable = model.time_dim
    x_time = model.ds[x_variable].values
    loc_ground = np.arange(len(x_time))+1
    xval = np.hstack(
        ([i*loc_ground[-1] + loc_ground for i in range(subcolumn_num)]))
    x_date2num = mdates.date2num([y for y in x_time])
    f = interpolate.interp1d(loc_ground, x_date2num, fill_value="extrapolate")
    xnew = xval / subcolumn_num
    input_time_long = f(xnew)
    input_time_2d_long = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        input_time_2d_long[j, :] = input_time_long

    y_variable = model.z_field
    y_height = model.ds[y_variable].values / 1000.  # km
    input_height_half = y_height[:, :, col_index]
    input_height_half_long = np.empty((lev_num, len(xval)))
    xval_2d = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        xval_2d[j, :] = xval/subcolumn_num
        for i in np.arange(len(x_time)):
            input_height_half_long[
                j, subcolumn_num * (i):subcolumn_num*(i+1) + 1] = input_height_half[i, j]

    Ze_tot = model.ds['sub_col_Ze_tot'][:, :, :, col_index].values
    beta_tot = model.ds['sub_col_beta_p_tot'][:, :, :, col_index].values
    Ze_tot_plt = np.transpose(Ze_tot, axes=(2, 1, 0)).reshape(lev_num, -1)
    beta_tot_plt = np.transpose(beta_tot, axes=(2, 1, 0)).reshape(lev_num, -1)
    x_dateformat = "%b%d-%H"
    x_rotation = 30

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(24*0.5, 12))
    fig.subplots_adjust(top=0.96, bottom=0.06, left=0.09,
                        right=0.9, wspace=0.1, hspace=0.2)
    ax = axes.flatten()
    cmap_plot = 'act_HomeyerRainbow'

    fontsize_input = 12
    plt.rcParams.update({'font.size': 12})

    textx, texty = 0.04, 1.03

    ifig = 0
    # var=np.transpose(dbze35_ground_th, axes=(0,2,1)).reshape(lev_ground.shape[0], -1)
    Ze_tot_plt[Ze_tot_plt <= -1.e+20] = np.nan
    c1 = ax[ifig].pcolormesh(input_time_2d_long, input_height_half_long,
                             Ze_tot_plt, vmin=-50, vmax=10, cmap=cmap_plot)
    ax[ifig].text(textx, texty, 'Radar', transform=ax[ifig].transAxes)
    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$Z_{e}$ [dBZ]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height [km]', fontsize=fontsize_input)

    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    vmin = 1e-8
    vmax = 1e-3

    ifig = 1
    beta_tot_plt[beta_tot_plt <= -1.e+40] = np.nan
    c1 = ax[ifig].pcolormesh(input_time_2d_long, input_height_half_long,
                             beta_tot_plt, norm=colors.LogNorm(vmin=vmin, vmax=vmax), cmap=cmap_plot)
    ax[ifig].text(textx, texty, 'Lidar', transform=ax[ifig].transAxes)
    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$\beta$ [$m^{-1} sr^{-1}$]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height [km]', fontsize=fontsize_input)
    ax[ifig].set_xlabel('Time [UTC]', fontsize=fontsize_input)
    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    if save_flag == 'save':
        fig.savefig(
            f'{fig_path}/radar_lidar_nonatt_allsubcols_{fig_name}.png', dpi=400)


# plot radar lidar signal with all subcolumns
def plot_every_subcolumn_timeseries_SR(model, atb_total_4D, atb_mol_4D, col_index, save_flag, fig_path, fig_name):
    """
    generate timeseries of lidar scattering ratio from every subcolumn.

    Parameters
    ----------
    model: func:`emc2.core.Model` class
        The model to read in some of pre-calculated variables.
    atb_total_4D: float
        lidar total attenuated backscatter coefficient, unit: :math:`m^{-1} sr^{-1}`
    atb_mol_4D: float
        lidar backscatter coefficient for molecuar, unit: :math:`m^{-1} sr^{-1}`
    col_index: int
        column index, unit: none
    save_flag: float
        0 or 1, if save (1) the figure or not (0)
    fig_path: string
        output figure directory
    fig_name: string
        output figure name
    """

    subcolumn_num = len(model.ds.subcolumn)
    lev_num = len(model.ds.lev)

    x_variable = model.time_dim
    x_time = model.ds[x_variable].values
    loc_ground = np.arange(len(x_time))+1
    xval = np.hstack(
        ([i*loc_ground[-1]+loc_ground for i in range(subcolumn_num)]))
    x_date2num = mdates.date2num([y for y in x_time])
    f = interpolate.interp1d(loc_ground, x_date2num, fill_value="extrapolate")
    xnew = xval/subcolumn_num
    input_time_long = f(xnew)
    input_time_2d_long = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        input_time_2d_long[j, :] = input_time_long

    y_variable = model.z_field
    y_height = model.ds[y_variable].values/1000.  # km
    input_height_half = y_height[:, :, col_index]
    input_height_half_long = np.empty((lev_num, len(xval)))
    xval_2d = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        xval_2d[j, :] = xval/subcolumn_num
        for i in np.arange(len(x_time)):
            input_height_half_long[
                j, subcolumn_num * (i):subcolumn_num*(i+1)+1] = input_height_half[i, j]

    beta_att_tot = atb_total_4D[:, :, :, col_index]
    beta_mol = atb_mol_4D[:, :, :, col_index]

    beta_att_tot_plt = np.transpose(
        beta_att_tot, axes=(2, 1, 0)).reshape(lev_num, -1)
    beta_mol_plt = np.transpose(beta_mol, axes=(2, 1, 0)).reshape(lev_num, -1)

    x_dateformat = "%b%d-%H"
    x_rotation = 30

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 12/2.))
    fig.subplots_adjust(top=0.96, bottom=0.06, left=0.09,
                        right=0.9, wspace=0.1, hspace=0.2)
    # ax=axes.flatten()
    cmap_plot = 'act_HomeyerRainbow'

    fontsize_input = 12
    plt.rcParams.update({'font.size': 12})

    textx, texty = 0.04, 1.03
    sr_model_level = beta_att_tot_plt/beta_mol_plt
    sr_model_level[sr_model_level <= -1.e+40] = np.nan
    c1 = ax.pcolormesh(input_time_2d_long, input_height_half_long,
                       sr_model_level, cmap=cmap_plot, vmin=0, vmax=80)
    ax.text(textx, texty, 'SR', transform=ax.transAxes)
    y1 = np.array(ax.get_position())[0, 1]
    ddy = np.array(ax.get_position())[1, 1]-np.array(ax.get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label('SR')
    ax.set_ylim(0, 15)
    ax.set_ylabel('Height [km]', fontsize=fontsize_input)
    ax.set_xlabel('Time [UTC]', fontsize=fontsize_input)

    ax.xaxis.set_major_formatter(mdates.DateFormatter(x_dateformat))
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    if save_flag == 'save':
        fig.savefig(
            f'{fig_path}/radar_lidar_SR_allsubcols_{fig_name}.png', dpi=400)


def plot_every_subcolumn_timeseries_mixingratio(model, col_index, save_flag, fig_path, fig_name):
    """
    Generate timeseries of mixing ratio from every subcolumn.

    Parameters
    ----------
    model: func:`emc2.core.Model` class
        The model to read in some of pre-calculated variables.
    col_index: int
        column index, unit: none
    save_flag: float
        0 or 1, if save (1) the figure or not (0)
    fig_path: string
        output figure directory
    fig_name: string
        output figure name

    """

    subcolumn_num = len(model.ds.subcolumn)
    lev_num = len(model.ds.lev)

    # prepare x and y axis values

    # time
    x_variable = model.time_dim
    x_time = model.ds[x_variable].values
    loc_ground = np.arange(len(x_time)) + 1
    xval = np.hstack(
        ([i*loc_ground[-1]+loc_ground for i in range(subcolumn_num)]))
    x_date2num = mdates.date2num([y for y in x_time])
    f = interpolate.interp1d(loc_ground, x_date2num, fill_value="extrapolate")
    xnew = xval/subcolumn_num
    input_time_long = f(xnew)
    input_time_2d_long = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        input_time_2d_long[j, :] = input_time_long

    # height
    y_variable = model.z_field
    y_height = model.ds[y_variable].values
    input_height_half = y_height[:, :, col_index]
    input_height_half_long = np.empty((lev_num, len(xval)))
    xval_2d = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        xval_2d[j, :] = xval/subcolumn_num
        for i in np.arange(len(x_time)):
            input_height_half_long[
                j, subcolumn_num * (i):subcolumn_num*(i+1)+1] = input_height_half[i, j]

    strat_q_subcolumns_cl = model.ds['strat_q_subcolumns_cl'][
        :, :, :, col_index].values
    strat_q_subcolumns_cl_plt = np.transpose(
        strat_q_subcolumns_cl, axes=(2, 1, 0)).reshape(lev_num, -1)

    strat_q_subcolumns_ci = model.ds['strat_q_subcolumns_ci'][
        :, :, :, col_index].values
    strat_q_subcolumns_ci_plt = np.transpose(
        strat_q_subcolumns_ci, axes=(2, 1, 0)).reshape(lev_num, -1)

    strat_q_subcolumns_pl = model.ds['strat_q_subcolumns_pl'][
        :, :, :, col_index].values
    strat_q_subcolumns_pl_plt = np.transpose(
        strat_q_subcolumns_pl, axes=(2, 1, 0)).reshape(lev_num, -1)

    strat_q_subcolumns_pi = model.ds['strat_q_subcolumns_pi'][
        :, :, :, col_index].values
    strat_q_subcolumns_pi_plt = np.transpose(
        strat_q_subcolumns_pi, axes=(2, 1, 0)).reshape(lev_num, -1)

    # plot

    x_dateformat = "%b%d-%H"
    x_rotation = 30

    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(24*0.5, 12*2.))
    fig.subplots_adjust(top=0.96, bottom=0.06, left=0.09,
                        right=0.9, wspace=0.1, hspace=0.2)
    ax = axes.flatten()
    cmap_plot = 'act_HomeyerRainbow'

    fontsize_input = 12
    plt.rcParams.update({'font.size': 12})

    textx, texty = 0.04, 1.03

    ifig = 0
    strat_q_subcolumns_cl_plt[strat_q_subcolumns_cl_plt <= 0] = np.nan
    c1 = ax[ifig].pcolormesh(input_time_2d_long, input_height_half_long/1000.,
                             strat_q_subcolumns_cl_plt*1000., vmin=0, vmax=0.1, cmap=cmap_plot)
    ax[ifig].text(textx, texty, 'strat_q_subcolumns_cl',
                  transform=ax[ifig].transAxes)

    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$q$ [[g/kg]]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height [km]', fontsize=fontsize_input)

    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    ifig = 1
    strat_q_subcolumns_ci_plt[strat_q_subcolumns_ci_plt <= 0] = np.nan
    c1 = ax[ifig].pcolormesh(input_time_2d_long, input_height_half_long/1000.,
                             strat_q_subcolumns_ci_plt*1000., vmin=0, vmax=0.01, cmap=cmap_plot)
    ax[ifig].text(textx, texty, 'strat_q_subcolumns_ci',
                  transform=ax[ifig].transAxes)
    # ax[ifig].set_xlabel('loc')
    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$q$ [g/kg]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height [km]', fontsize=fontsize_input)

    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    ifig = 2
    strat_q_subcolumns_pl_plt[strat_q_subcolumns_pl_plt <= 0] = np.nan
    c1 = ax[ifig].pcolormesh(input_time_2d_long, input_height_half_long/1000.,
                             strat_q_subcolumns_pl_plt*1000., vmin=0, vmax=0.01, cmap=cmap_plot)
    ax[ifig].text(textx, texty, 'strat_q_subcolumns_pl',
                  transform=ax[ifig].transAxes)
    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$q$ [g/kg]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height [km]', fontsize=fontsize_input)

    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    ifig = 3
    strat_q_subcolumns_pi_plt[strat_q_subcolumns_pi_plt <= 0] = np.nan
    c1 = ax[ifig].pcolormesh(input_time_2d_long, input_height_half_long/1000.,
                             strat_q_subcolumns_pi_plt*1000., vmin=0, vmax=0.1, cmap=cmap_plot)
    ax[ifig].text(textx, texty, 'strat_q_subcolumns_pi',
                  transform=ax[ifig].transAxes)
    # ax[ifig].set_xlabel('loc')
    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$q$ [g/kg]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height [km]', fontsize=fontsize_input)
    ax[ifig].set_xlabel('Time (UTC)', fontsize=fontsize_input)

    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    if save_flag == 'save':
        fig.savefig(f'{fig_path}/q_allsubcols_{fig_name}.png', dpi=400)


def plot_every_subcolumn_timeseries_mixingratio_cloud_precipitation(model, col_index, save_flag, fig_path, fig_name):
    """
    Generate timeseries of cloud and precipitation mixing ratios from every subcolumn.

    Parameters
    ----------
    model: func:`emc2.core.Model` class
        The model to read in some of pre-calculated variables.
    atb_total_4D: float
        lidar total attenuated backscatter coefficient, unit: m^{-1} sr^{-1}
    atb_mol_4D: float
        lidar backscatter coefficient for molecuar, unit: m^{-1} sr^{-1}
    col_index: int
        column index, unit: none
    save_flag: float
        0 or 1, if save (1) the figure or not (0)
    fig_path: string
        output figure directory
    fig_name: string
        output figure name
    """

    subcolumn_num = len(model.ds.subcolumn)
    lev_num = len(model.ds.lev)

    # prepare x and y axis values
    # time
    subcolumn_num = len(model.ds.subcolumn)
    x_variable = model.time_dim
    x_time = model.ds[x_variable].values
    loc_ground = np.arange(len(x_time)) + 1
    xval = np.hstack(
        ([i*loc_ground[-1]+loc_ground for i in range(subcolumn_num)]))
    x_date2num = mdates.date2num([y for y in x_time])
    f = interpolate.interp1d(loc_ground, x_date2num, fill_value="extrapolate")
    xnew = xval/subcolumn_num
    input_time_long = f(xnew)
    input_time_2d_long = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        input_time_2d_long[j, :] = input_time_long

    # height
    y_variable = model.z_field
    y_height = model.ds[y_variable].values
    input_height_half = y_height[:, :, col_index]
    input_height_half_long = np.empty((lev_num, len(xval)))
    xval_2d = np.empty((lev_num, len(xval)))
    for j in np.arange(lev_num):
        xval_2d[j, :] = xval/subcolumn_num
        for i in np.arange(len(x_time)):
            input_height_half_long[
                j, subcolumn_num * (i):subcolumn_num*(i+1)+1] = input_height_half[i, j]

    strat_q_subcolumns_cl = model.ds['strat_q_subcolumns_cl'][
        :, :, :, col_index].values
    strat_q_subcolumns_cl_plt = np.transpose(
        strat_q_subcolumns_cl, axes=(2, 1, 0)).reshape(lev_num, -1)

    strat_q_subcolumns_ci = model.ds['strat_q_subcolumns_ci'][
        :, :, :, col_index].values
    strat_q_subcolumns_ci_plt = np.transpose(
        strat_q_subcolumns_ci, axes=(2, 1, 0)).reshape(lev_num, -1)

    strat_q_subcolumns_pl = model.ds['strat_q_subcolumns_pl'][
        :, :, :, col_index].values
    strat_q_subcolumns_pl_plt = np.transpose(
        strat_q_subcolumns_pl, axes=(2, 1, 0)).reshape(lev_num, -1)

    strat_q_subcolumns_pi = model.ds['strat_q_subcolumns_pi'][
        :, :, :, col_index].values
    strat_q_subcolumns_pi_plt = np.transpose(
        strat_q_subcolumns_pi, axes=(2, 1, 0)).reshape(lev_num, -1)

    # plot

    x_dateformat = "%b%d-%H"
    x_rotation = 30

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(24*0.5, 12))
    fig.subplots_adjust(top=0.96, bottom=0.06, left=0.09,
                        right=0.9, wspace=0.1, hspace=0.2)
    ax = axes.flatten()
    cmap_plot = 'act_HomeyerRainbow'

    fontsize_input = 12
    plt.rcParams.update({'font.size': 12})

    textx, texty = 0.04, 1.03
    ifig = 0
    plot_var0 = strat_q_subcolumns_cl_plt+strat_q_subcolumns_ci_plt
    plot_var0[plot_var0 < 0] = np.nan
    c1 = ax[ifig].pcolormesh(
        input_time_2d_long, input_height_half_long / 1000.,
        plot_var0*1000., vmin=0, vmax=0.1, cmap=cmap_plot)
    ax[ifig].text(textx, texty, '(a) Cloud', transform=ax[ifig].transAxes)
    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$q$ [g/kg]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height [km]', fontsize=fontsize_input)

    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    ifig = 1
    plot_var1 = strat_q_subcolumns_pl_plt+strat_q_subcolumns_pi_plt
    plot_var1[plot_var1 < 0] = np.nan
    c1 = ax[ifig].pcolormesh(
        input_time_2d_long, input_height_half_long / 1000.,
        plot_var1*1000., vmin=0, vmax=0.1, cmap=cmap_plot)
    ax[ifig].text(textx, texty, '(b) Precipitation',
                  transform=ax[ifig].transAxes)
    y1 = np.array(ax[ifig].get_position())[0, 1]
    ddy = np.array(ax[ifig].get_position())[1, 1] - \
        np.array(ax[ifig].get_position())[0, 1]
    cb_ax = fig.add_axes([0.91, y1, 0.02, ddy])
    clb = fig.colorbar(c1, cax=cb_ax)
    clb.set_label(r'$q$ [g/kg]')
    ax[ifig].set_ylim(0, 15)
    ax[ifig].set_ylabel('Height (km)', fontsize=fontsize_input)
    ax[ifig].set_xlabel('Time (UTC)', fontsize=fontsize_input)

    subplot_index = ifig
    ax[subplot_index].xaxis.set_major_formatter(
        mdates.DateFormatter(x_dateformat))
    for label in ax[subplot_index].get_xticklabels(which='major'):
        label.set(rotation=x_rotation, horizontalalignment='right')

    if save_flag == 'save':
        fig.savefig(
            f'{fig_path}/q_cloud_precipitation_allsubcols_{fig_name}.png', dpi=400)
