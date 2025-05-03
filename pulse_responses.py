import numpy as np
import matplotlib.pyplot as plt
import util
import nd2
import os

exp = '20250502'
culture = 'culture2'
trial = 'trial0'

trial_subpath = f'{exp}/{culture}/{trial}'
# local_data_dir = 'D:\\User\\AG_Dean\\Hana_Sheldon'
local_data_dir = './data'
remote_data_dir = '/home/khzstimpi/data'

trial_dir = os.path.join(local_data_dir,trial_subpath)
if not os.path.exists(os.path.join(trial_dir, 'sample.bin')):
    os.system(f'scp -r khzstimpi@khzstimpi:{remote_data_dir}/{trial_subpath}/* {trial_dir}')

    
print('Loading electric field data')
efield, sample_times, frame_times, settings = util.load_stim_data(trial_dir, subsampling_factor=32)

mod_period = 1.0/settings['mod_frequency']        
mod_periods_per_block = int(np.ceil(settings['block_duration']/mod_period))
    
t = float(settings['nostim_pre_post_duration'])
pulse_times = []
for phase in settings['phases']:
    t_pulse = t + (mod_periods_per_block-1) * mod_period + mod_period*phase/360
    pulse_times.append(t_pulse)
    t += mod_periods_per_block * mod_period + settings['nostim_interblock_duration']


print('Loading microscopy data')
raw = nd2.imread(trial_dir + '/raw.nd2')
print(raw.shape)
