import numpy as np

buffer_size = 16384
electrode_spacing = 10E-3
amplifier_gain_level = 1
vref = 10

def get_amplifier_gain(level):
    gains = [1, 5, 10, 50, 100, 200]
    return gains[level-1]

def load_stim_data(trial_dir, subsampling_factor=32, sampling_rate=400000, buffer_size=16384,
              electrode_spacing=10E-3, amplifier_gain_level=1, vref=10):
    
    sample_data = np.fromfile(trial_dir + '/sample.bin', dtype=np.uint16)
    settings = np.load(trial_dir + '/settings.npz')
    
    sample_data = sample_data[buffer_size*2:]

    if subsampling_factor > 1:
        sample_data = sample_data[::subsampling_factor]
        sampling_rate = sampling_rate / subsampling_factor
    
    adc_voltages = - \
        ((((sample_data & 4095).astype(np.float32)-2048)/2048) * vref)
    applied_efield = (
        adc_voltages / get_amplifier_gain(amplifier_gain_level)) / electrode_spacing
    din0 = (sample_data & (1 << 13)) >> 13
    # din1 = (sample_data & (1 << 14)) >> 14

    t = np.arange(0, len(applied_efield), dtype=np.float32) / sampling_rate

    frame_indices = np.where(np.diff(din0) == 1)[0]
    frame_times = t[frame_indices]

    return applied_efield, t, frame_times, settings
