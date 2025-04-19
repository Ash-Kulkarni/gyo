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
) => {
  console.log("equipModuleFromInventory");
};
const unequipModule = (equippedModules, inventory, equippedIndex) => {
  console.log("unequipModule");
};
const editModulePosition = (equippedModules, equippedIndex, position) => {
  console.log("editModulePosition");
};
const editModuleAim = (equippedModules, equippedIndex, aim) => {
  console.log("editModuleAim");
};
const saveModule = (equippedModules, equippedIndex) => {
  console.log("saveModule");
};

export function handleEditorInput(input, player, inventory) {
  // console.log("Editor input:", input);
  const equippedModules = player.modules;
  // console.log(equippedModules);
  // console.log(inventory);

  switch (editorState.mode) {
    case EDITOR_MODE.INVENTORY:
      if (input[EDITOR_KEYMAP.A_KEY]) {
        equipModuleFromInventory(
          equippedModules,
          inventory,
          editorState.inventoryIndex,
        );
      } else if (input[EDITOR_KEYMAP.DPAD_UP_KEY]) {
        editorState.inventoryIndex =
          (editorState.inventoryIndex - 1 + inventory.length) %
          inventory.length;
      } else if (input[EDITOR_KEYMAP.DPAD_DOWN_KEY]) {
        editorState.inventoryIndex =
          (editorState.inventoryIndex + 1) % inventory.length;
      } else if (input[EDITOR_KEYMAP.RIGHT_BUMPER_KEY]) {
        editorState.mode = EDITOR_MODE.EQUIPPED;
      }
      break;

    case EDITOR_MODE.EQUIPPED:
      if (equippedModules.length === 0) {
        editorState.mode = EDITOR_MODE.INVENTORY;
        return;
      }
      if (input[EDITOR_KEYMAP.A_KEY]) {
        editorState.mode = EDITOR_MODE.POSITION_EDIT;
      } else if (input[EDITOR_KEYMAP.DPAD_RIGHT_KEY]) {
        editorState.equippedIndex =
          (editorState.equippedIndex + 1) % equippedModules.length;
      } else if (input[EDITOR_KEYMAP.DPAD_LEFT_KEY]) {
        editorState.equippedIndex =
          (editorState.equippedIndex - 1 + equippedModules.length) %
          equippedModules.length;
      } else if (input[EDITOR_KEYMAP.B_KEY]) {
        unequipModule(equippedModules, inventory, editorState.equippedIndex);
      } else if (input[EDITOR_KEYMAP.LEFT_BUMPER_KEY]) {
        editorState.mode = EDITOR_MODE.INVENTORY;
      }
      break;

    case EDITOR_MODE.POSITION_EDIT:
      if (input[EDITOR_KEYMAP.DPAD_UP_KEY]) {
        editModulePosition(equippedModules, editorState.equippedIndex, "up");
      } else if (input[EDITOR_KEYMAP.DPAD_DOWN_KEY]) {
        editModulePosition(equippedModules, editorState.equippedIndex, "down");
      } else if (input[EDITOR_KEYMAP.DPAD_LEFT_KEY]) {
        editModulePosition(equippedModules, editorState.equippedIndex, "left");
      } else if (input[EDITOR_KEYMAP.DPAD_RIGHT_KEY]) {
        editModulePosition(equippedModules, editorState.equippedIndex, "right");
      } else if (input[EDITOR_KEYMAP.B_KEY]) {
        editorState.mode = EDITOR_MODE.EQUIPPED;
      } else if (input[EDITOR_KEYMAP.A_KEY]) {
        editorState.mode = EDITOR_MODE.AIM_EDIT;
      }
      break;

    case EDITOR_MODE.AIM_EDIT:
      if (input[EDITOR_KEYMAP.DPAD_UP_KEY]) {
        editModuleAim(equippedModules, editorState.equippedIndex, "up");
      } else if (input[EDITOR_KEYMAP.DPAD_DOWN_KEY]) {
        editModuleAim(equippedModules, editorState.equippedIndex, "down");
      } else if (input[EDITOR_KEYMAP.DPAD_LEFT_KEY]) {
        editModuleAim(equippedModules, editorState.equippedIndex, "left");
      } else if (input[EDITOR_KEYMAP.DPAD_RIGHT_KEY]) {
        editModuleAim(equippedModules, editorState.equippedIndex, "right");
      } else if (input[EDITOR_KEYMAP.B_KEY]) {
        editorState.mode = EDITOR_MODE.EQUIPPED;
      } else if (input[EDITOR_KEYMAP.A_KEY]) {
        saveModule(equippedModules, editorState.equippedIndex);
        editorState.mode = EDITOR_MODE.EQUIPPED;
      }
      // A to save and return to equipped_selection
      break;
  }
}
