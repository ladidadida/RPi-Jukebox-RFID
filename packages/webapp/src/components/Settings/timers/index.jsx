import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import {
  Card,
  CardContent,
  CardHeader,
  Divider,
  Grid,
  List,
} from '@mui/material';

import Timer from './timer';
import request from '../../../utils/request';

// Timers whose action is unavailable (e.g. shutdown without the raspberry-pi plugin) are hidden.
const SettingsTimers = () => {
  const { t } = useTranslation();
  const [timers, setTimers] = useState([]);

  useEffect(() => {
    const fetchTimers = async () => {
      const { result } = await request('listTimers');
      if (result) {
        setTimers(result.filter(timer => timer.available));
      }
    };

    fetchTimers();
  }, []);

  if (timers.length === 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader
        title={t('settings.timers.title')}
      />
      <Divider />
      <CardContent>
        <Grid size={12}>
          <List>
            {timers.map(timer => <Timer key={timer.name} timer={timer} />)}
          </List>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default SettingsTimers;
