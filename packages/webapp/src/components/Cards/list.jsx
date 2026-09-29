import { forwardRef, memo } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import {
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemButton,
  ListItemText,
  Typography
} from '@mui/material';

import BookmarkIcon from '@mui/icons-material/Bookmark';

const CardsList = ({ cardsList }) => {
  const { t } = useTranslation();

  const ListItemLink = (cardId) => {
    const card = cardsList[cardId];
    const EditCardLink = forwardRef((props, ref) => {
      return (
        <Link
          ref={ref}
          state={{ id: cardId, ...card }}
          to={`/cards/${cardId}/edit`}
          {...props}
        />
      );
    });
    EditCardLink.displayName = 'EditCardLink';

    const args = Object.values(card.args || {}).join(', ');
    const description = card.error
      ? `⚠️ ${card.action || ''} ${card.error}`.trim()
      : [card.action, args].filter(Boolean).join(': ');

    return (
      <ListItem disablePadding key={cardId}>
        <ListItemButton component={EditCardLink} nativeButton={false}>
          <ListItemAvatar>
            <Avatar>
              <BookmarkIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText
            primary={cardId}
            secondary={description}
          />
        </ListItemButton>
      </ListItem>
    );
  }

  return (
    cardsList && Object.keys(cardsList).length > 0
      ? <List sx={{ width: '100%' }}>
          {Object.keys(cardsList).map(ListItemLink)}
        </List>
      : <Typography>{t('cards.list.no-cards-registered')}</Typography>
  );
}

export default memo(CardsList);
