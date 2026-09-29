
import { Grid } from '@mui/material';

import SettingsAudio from './audio';
import SettingsGeneral from './general';
import SettingsSecondSwipe from './secondswipe';
import SettingsStatus from './status/index';
import SettingsTimers from './timers';

import { useTheme } from '@mui/material/styles';

const Settings = () => {
  const theme = useTheme();
  const spacer = { marginBottom: theme.spacing(1) }

  return (
    <Grid
      container
      id="settings"
      sx={{
        '& > :not(:last-child)': spacer,
        flexDirection: 'column',
        padding: '10px',
      }}
    >
      <Grid>
        <SettingsStatus />
      </Grid>
      <Grid>
        <SettingsGeneral />
      </Grid>
      <Grid>
        <SettingsAudio />
      </Grid>
      <Grid>
        <SettingsTimers />
      </Grid>
      <Grid>
        <SettingsSecondSwipe />
      </Grid>
    </Grid>
  );
};

export default Settings;
