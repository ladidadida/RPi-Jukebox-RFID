import { useContext } from 'react';
import { useTranslation } from 'react-i18next';

import {
  Box,
  ListItem,
  ListItemText,
  LinearProgress,
} from '@mui/material';

import PubSubContext from '../../../context/pubsub/context';
import { SYSTEM_HEALTH_TOPIC } from '../../../config';

const toGb = (bytes) => (bytes / 1e9).toFixed(1);

const StatusDiskUsage = () => {
  const { t } = useTranslation();
  const { state: { [SYSTEM_HEALTH_TOPIC]: health } } = useContext(PubSubContext);

  if (!health?.disk_total) {
    return null;
  }

  const percentage = Math.round(health.disk_used / health.disk_total * 100);

  return (
    <ListItem
      disableGutters
      sx={{ display: 'flex', flexDirection: 'column' }}
    >
      <Box sx={{ width: '100%' }}>
        <LinearProgress variant="determinate" value={percentage} />
      </Box>
      <ListItemText
        sx={{ width: '100%' }}
        primary={t('settings.status.disk-usage.result', {
          used: toGb(health.disk_used),
          total: toGb(health.disk_total),
          result: percentage,
        })}
        secondary={t('settings.status.disk-usage.label')}
      />
    </ListItem>
  );
};

export default StatusDiskUsage;
