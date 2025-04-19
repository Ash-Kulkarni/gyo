import { EDITOR_KEYMAP } from "../input";
import { sendInput } from "../net.js";

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
//

const equipModuleFromInventory = (
  equippedModules,
  inventory,
  inventoryIndex,
) => {};
const unequipModule = (equippedModules, inventory, equippedIndex) => {};
const editModulePosition = (equippedModules, equippedIndex, position) => {};
const editModuleAim = (equippedModules, equippedIndex, aim) => {};

export function handleEditorInput(input, player, inventory) {
  // console.log("Editor input:", input);
  const mods = player.modules;
  // console.log(mods);
  // console.log(inventory);

  switch (editorState.mode) {
    case "inventory":
      if (input[EDITOR_KEYMAP.A_KEY]) {
        // A to equip
        editorState.mode = "equipped_selection";
        console.log("Equipping item");
      }
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
