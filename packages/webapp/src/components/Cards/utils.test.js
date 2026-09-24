import { expect, test } from 'vitest';

import commands from '../../commands';
import {
  buildActionData,
  getArgsValues,
} from './utils';


test('player card contracts preserve provider-qualified content', () => {
  expect(commands.play_single.argKeys).toEqual(['song_url', 'provider']);
  expect(commands.play_album.argKeys).toEqual([
    'albumartist',
    'album',
    'content_uri',
    'provider',
  ]);

  const providerAlbum = buildActionData('play_music', 'play_album', {
    albumartist: 'Artist',
    album: 'Album',
    content_uri: 'service:album:123',
    provider: 'streaming',
  });
  expect(getArgsValues(providerAlbum)).toEqual([
    'Artist',
    'Album',
    'service:album:123',
    'streaming',
  ]);

  const legacyAlbum = buildActionData(
    'play_music',
    'play_album',
    ['Artist', 'Album'],
  );
  expect(getArgsValues(legacyAlbum)).toEqual([
    'Artist',
    'Album',
    undefined,
    undefined,
  ]);
});
