import { EDITOR_KEYMAP } from "../input";
import { sendInput } from "../net.js";

export const EDITOR_MODE = {
  INVENTORY: "inventory",
  EQUIPPED: "equipped",
  POSITION_EDIT: "position_edit",
  AIM_EDIT: "aim_edit",
};

export const editorState = {
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
  // const item = inventory[inventoryIndex];
  // if (!item) return;
  // equippedModules.push(item);
  // equippedModules.push({...item})
  sendInput({
    event: "equip_module",
    module_id: inventory[inventoryIndex].module_id,
  });
};
const unequipModule = (equippedModules, inventory, equippedIndex) => {
  sendInput({
    event: "unequip_module",
    module_id: equippedModules[equippedIndex].module_id,
  });
  console.log("unequipModule");
};
const editModulePosition = (
  equippedModules,
  equippedIndex,
  { offset_angle = undefined, distance = undefined },
) => {
  if (offset_angle === undefined && distance === undefined) return;
  sendInput({
    event: "edit_module_position",
    module_id: equippedModules[equippedIndex].module_id,
    data: { offset_angle, distance },
  });
  console.log("editModulePosition");
};
const editModuleAim = (
  equippedModules,
  equippedIndex,
  { aim_angle = undefined },
) => {
  if (aim_angle === undefined) return;
  sendInput({
    event: "edit_module_aim",
    module_id: equippedModules[equippedIndex].module_id,
    data: { aim_angle },
  });
  console.log("editModuleAim");
};
const saveModule = (equippedModules, equippedIndex) => {
  // sendInput({ event: "save_module", module_id: equippedModules[equippedIndex].module_id });
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
      } else if (input[EDITOR_KEYMAP.DPAD_RIGHT_KEY]) {
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
      } else if (input[EDITOR_KEYMAP.DPAD_DOWN_KEY]) {
        editorState.equippedIndex =
          (editorState.equippedIndex + 1) % equippedModules.length;
      } else if (input[EDITOR_KEYMAP.DPAD_UP_KEY]) {
        editorState.equippedIndex =
          (editorState.equippedIndex - 1 + equippedModules.length) %
          equippedModules.length;
      } else if (input[EDITOR_KEYMAP.B_KEY]) {
        unequipModule(equippedModules, inventory, editorState.equippedIndex);
      } else if (input[EDITOR_KEYMAP.DPAD_LEFT_KEY]) {
        editorState.mode = EDITOR_MODE.INVENTORY;
      }
      break;

    case EDITOR_MODE.POSITION_EDIT:
      const selectedModule = player.modules[editorState.equippedIndex];
      const selectedModuleDistance = selectedModule.distance;
      const selectedModuleOffsetAngle = selectedModule.offset_angle;
      if (input[EDITOR_KEYMAP.DPAD_UP_KEY]) {
        editModulePosition(equippedModules, editorState.equippedIndex, {
          distance: selectedModuleDistance + 1,
        });
      } else if (input[EDITOR_KEYMAP.DPAD_DOWN_KEY]) {
        editModulePosition(equippedModules, editorState.equippedIndex, {
          distance: selectedModuleDistance - 1,
        });
      } else if (input[EDITOR_KEYMAP.DPAD_LEFT_KEY]) {
        editModulePosition(equippedModules, editorState.equippedIndex, {
          offset_angle: selectedModuleOffsetAngle - 0.1,
        });
      } else if (input[EDITOR_KEYMAP.DPAD_RIGHT_KEY]) {
        editModulePosition(equippedModules, editorState.equippedIndex, {
          offset_angle: selectedModuleOffsetAngle + 0.1,
        });
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
