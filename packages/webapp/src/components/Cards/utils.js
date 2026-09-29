import {
  isEmpty,
  has,
} from 'ramda';

import commands from '../../commands';
import { JUKEBOX_ACTIONS_MAP } from '../../config';

const mapValuesToKeys = (command, args) => {
  const argKeys = getCommandArgKeys(command);
  const values = argKeys.reduce((prev, arg, pos) => (
    {
      ...prev,
      [arg]: args[pos],
    }
    ), {});

  return values;
};

const getActionAndCommand = (actionData) => {
  const { action, command: { name } = {} } = actionData;

  return { action, command: name };
}

const findActionByCommand = (command) => {
  const action = Object.keys(JUKEBOX_ACTIONS_MAP).find((action) => {
    return has(command)(JUKEBOX_ACTIONS_MAP[action].commands)
  });

  return action;
};

const getCommandArgKeys = (command) => {
  const { [command] : { argKeys = [] } = {} } = commands;

  return argKeys;
};

const buildActionData = (action, command = {}, args = {}) => {
  const data = {
    action,
    command,
  };

  if (!isEmpty(command)) {
    const _args = Array.isArray(args)
      ? mapValuesToKeys(command, args)
      : args;

    data.command = {
      name: command,
      args: _args,
    }
  }

  return data;
};

const findCommandByCardAction = (cardAction) => (
  Object.keys(commands).find(command => commands[command].cardAction === cardAction)
);

// The card entry to register for the selected command: `{ action, args }` with named args.
const buildCardEntry = (actionData) => {
  const { command } = getActionAndCommand(actionData);
  const argKeys = getCommandArgKeys(command);
  const values = getArgsValues(actionData);
  const args = argKeys.reduce((prev, key, pos) => (
    values[pos] === undefined ? prev : { ...prev, [key]: values[pos] }
  ), {});

  return { action: commands[command]?.cardAction, args };
};

const getArgsValues = (actionData) => {
  const { command } = getActionAndCommand(actionData);
  const argKeys = getCommandArgKeys(command);
  const { [command]: { argDefaults = {} } = {} } = commands;

  return argKeys.map(
    key => (
      actionData.command.args[key] === undefined
        ? argDefaults[key]
        : actionData.command.args[key]
    )
  );
};

export {
  buildActionData,
  buildCardEntry,
  findActionByCommand,
  findCommandByCardAction,
  getActionAndCommand,
  getArgsValues,
};
