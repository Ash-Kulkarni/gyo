const EDITOR_MODE = {
  INVENTORY: "inventory",
  EQUIPPED: "equipped",
  POSITION_EDIT: "position_edit",
  AIM_EDIT: "aim_edit",
};

const editorState = {
  mode: EDITOR_MODE.INVENTORY,
  inventoryIndex: 0,
  equippedIndex: 0,
};

// TODO
export function handleEditorInput(input, player) {
  console.log("Editor input:", input);
  const mods = player.modules;

  switch (editorState.mode) {
    case "inventory":
      // up/down to change selection
      // A to equip
      // left/right to change equipped
      break;

    case "equipped_selection":
      // left/right to select equipped
      // B to go back to inventory
      // A to enter POSITION_EDIT
      break;

    case "edit_position":
      // left/right to rotate
      // up/down to change distance
      // A to enter AIM_EDIT
      break;

    case "edit_aim":
      // left/right to rotate aim
      // B to return to POSITION_EDIT
      // A to save and return to equipped_selection
      break;
  }
}
