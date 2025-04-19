export const VIEW = {
  MAIN_MENU: "main_menu",
  PLAYING: "playing",
  EDITOR: "editor",
  LEVEL_END: "level_end",
};

export const uiState = {
  currentView: VIEW.PLAYING,
};

export function setCurrentView(view) {
  uiState.currentView = view;
}
