import CommandSelector from '../../command-selector';

const SelectHost = ({
  actionData,
  handleActionDataChange,
}) => (
  <CommandSelector
    actionData={actionData}
    handleActionDataChange={handleActionDataChange}
  />
);

export default SelectHost;
