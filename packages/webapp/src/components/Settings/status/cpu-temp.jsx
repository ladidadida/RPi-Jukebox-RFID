import { useContext } from 'react';
import { useTranslation } from 'react-i18next';

import {
  ListItem,
  ListItemText,
} from '@mui/material';

import PubSubContext from '../../../context/pubsub/context';
import { SYSTEM_HEALTH_TOPIC } from '../../../config';

const StatusCpuTemp = () => {
  const { t } = useTranslation();
  const { state: { [SYSTEM_HEALTH_TOPIC]: health } } = useContext(PubSubContext);

  if (health?.cpu_temperature == null) {
    return null;
  }

  return (
    <ListItem disableGutters>
      <ListItemText
        primary={`${health.cpu_temperature}°C`}
        secondary={t('settings.status.cpu-temp.label')}
      />
    </ListItem>
  );
};

export default StatusCpuTemp;
