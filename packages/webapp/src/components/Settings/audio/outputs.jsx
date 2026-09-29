import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import {
  CircularProgress,
  Grid,
  FormControl,
  FormControlLabel,
  Radio,
  RadioGroup,
  Typography,
} from '@mui/material';

import request from '../../../utils/request';

const Outputs = () => {
  const { t } = useTranslation();

  const [active, setActive] = useState(null);
  const [outputs, setOutputs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  const setOutput = async (event, name) => {
    setActive(name);
    setIsLoading(true);
    const { error } = await request('setAudioOutput', { name });
    setIsLoading(false);
    setIsError(Boolean(error));
  };

  useEffect(() => {
    const fetchAudioOutputs = async () => {
      const { result, error } = await request('getAudioOutputs');
      setIsLoading(false);

      if (error) {
        setIsError(true);
        return console.error(error);
      }

      setActive(result.active);
      setOutputs(result.outputs);
    };

    fetchAudioOutputs();
  }, []);

  return (
    <Grid container sx={{ flexDirection: 'column' }}>
      <Grid
        container
        sx={{
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Typography>{t('settings.audio.outputs.title')}</Typography>
        {isLoading && <CircularProgress size={20} />}
        {isError && <Typography>⚠️</Typography>}
      </Grid>
      <FormControl component="fieldset">
        <RadioGroup
          aria-label={t('settings.audio.outputs.title')}
          name="audio-outputs"
          value={active ?? ''}
          onChange={setOutput}
        >
          {outputs.map(({ alias, name }) =>
            <FormControlLabel
              control={<Radio />}
              label={alias}
              key={name}
              value={name}
            />
          )}
        </RadioGroup>
      </FormControl>
    </Grid>
  );
};

export default Outputs;
