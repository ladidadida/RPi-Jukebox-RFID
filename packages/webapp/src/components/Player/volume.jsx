import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import Grid from '@mui/material/Grid';
import Slider from '@mui/material/Slider';
import VolumeDownIcon from '@mui/icons-material/VolumeDown';
import VolumeMuteIcon from '@mui/icons-material/VolumeMute';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import { useTheme } from '@mui/material/styles';

import request from '../../utils/request';

const Volume = () => {
  const theme = useTheme();
  const { t } = useTranslation();

  const [isChangingVolume, setIsChangingVolume] = useState(false);
  const [_volume, setVolume] = useState(0);
  const [volumeStep] = useState(1);

  const updateVolume = () => {
    request('setVolume', { volume: _volume });
    // Delay the next command to avoid jumping slide control
    setTimeout(() => setIsChangingVolume(false), 500);
  }

  const handleVolumeChange = (event, newVolume) => {
    setIsChangingVolume(true);
    setVolume(newVolume);
  }

  useEffect(() => {
    const fetchVolume = async () =>  {
      const { result } = await request('getVolume');
      if (result?.volume !== undefined && !isChangingVolume) {
        setVolume(result.volume);
      }
    }

    fetchVolume();
  }, [isChangingVolume]);

  return (
    <Grid
      container
      sx={{ alignItems: 'center', width: '100%' }}
    >
      <Grid sx={{ marginRight: theme.spacing(1), display: 'flex' }} title={t('player.volume.slider')}>
        {_volume === 0 && <VolumeMuteIcon />}
        {_volume > 0 && _volume < 50 && <VolumeDownIcon />}
        {_volume >= 50 && <VolumeUpIcon />}
      </Grid>
      <Grid size="grow" sx={{ marginTop: theme.spacing(1) }}>
        <Slider
          aria-labelledby={t('player.volume.slider')}
          onChange={handleVolumeChange}
          onChangeCommitted={updateVolume}
          step={volumeStep}
          value={_volume}
          valueLabelDisplay="auto"
        />
      </Grid>
    </Grid>
  );
}

export default Volume;
