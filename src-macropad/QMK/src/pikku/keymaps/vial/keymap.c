// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H
// Layer Names
enum layer_names {
    _BASE,
    _TEAMS,
    _CODE,
    _GIT,
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /*
     * ├───┼───┼───┼
     * │ 4 │ 5 │ 6 │
     * ├───┼───┼───┼
     * │ 1 │ 2 │ 3 │
     * ├───┼───┼───┼

     */
    [0] = LAYOUT_default_2x3(
        TO(1),   KC_P5,   KC_P6,
        KC_P1,   KC_P2,   KC_P3
    ),
    [1] = LAYOUT_default_2x3(
        TO(2),   KC_P1,   KC_P1,
        KC_P1,   KC_P1,   KC_P1
    ),
    [2] = LAYOUT_default_2x3(
        TO(3),   KC_P2,   KC_P2,
        KC_P1,   KC_P2,   KC_P2
    ),
    [3] = LAYOUT_default_2x3(
        TO(0),   KC_P3,   KC_P3,
        KC_P3,   KC_P3,   KC_P3
    )
};

#ifdef OLED_ENABLE
void write_caps_status(void){
    led_t led_state = host_keyboard_led_state();
    oled_write_ln_P(led_state.caps_lock ? PSTR("CAPS") : PSTR("    "), false);
}

// Draw to OLED
bool oled_task_user() {
    oled_set_cursor(0,0);
    write_caps_status();
    oled_write_P(PSTR("Current Layer: "), false);
    switch(get_highest_layer(layer_state)){
        case _BASE:
            oled_write_ln_P(PSTR("Base"), false);
            break;
        case _TEAMS:
            oled_write_ln_P(PSTR("Teams"), false);
            break;
        case _CODE:
            oled_write_ln_P(PSTR("Code"), false);
            break;
        case _GIT:
            oled_write_ln_P(PSTR("Git"), false);
            break;

    }
    return false;
}
#endif