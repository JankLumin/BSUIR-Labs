#!/bin/bash

shopt -s extglob

RESET=$'\033[0m'
COLOR_2=$'\033[1;37m'       # Белый
COLOR_4=$'\033[1;36m'       # Голубой
COLOR_8=$'\033[1;34m'       # Синий
COLOR_16=$'\033[1;32m'      # Зеленый
COLOR_32=$'\033[1;33m'      # Желтый
COLOR_64=$'\033[1;35m'      # Фиолетовый
COLOR_128=$'\033[1;31m'     # Красный
COLOR_256=$'\033[0;32m'     # Темно-зеленый
COLOR_512=$'\033[0;33m'     # Темно-желтый
COLOR_1024=$'\033[0;36m'    # Темно-голубой
COLOR_2048=$'\033[0;34m'    # Темно-синий
COLOR_4096=$'\033[0;35m'    # Темно-фиолетовый
COLOR_8192=$'\033[0;37m'    # Серый
COLOR_16384=$'\033[1;90m'   # Светло-серый
COLOR_32768=$'\033[1;91m'   # Светло-красный
COLOR_65536=$'\033[1;92m'   # Светло-зеленый
COLOR_131072=$'\033[1;93m'  # Светло-желтый
COLOR_DEFAULT=$'\033[1;94m' # Светло-синий

get_color() {
    case "$1" in
        2) echo -n "$COLOR_2" ;;
        4) echo -n "$COLOR_4" ;;
        8) echo -n "$COLOR_8" ;;
        16) echo -n "$COLOR_16" ;;
        32) echo -n "$COLOR_32" ;;
        64) echo -n "$COLOR_64" ;;
        128) echo -n "$COLOR_128" ;;
        256) echo -n "$COLOR_256" ;;
        512) echo -n "$COLOR_512" ;;
        1024) echo -n "$COLOR_1024" ;;
        2048) echo -n "$COLOR_2048" ;;
        4096) echo -n "$COLOR_4096" ;;
        8192) echo -n "$COLOR_8192" ;;
        16384) echo -n "$COLOR_16384" ;;
        32768) echo -n "$COLOR_32768" ;;
        65536) echo -n "$COLOR_65536" ;;
        131072) echo -n "$COLOR_131072" ;;
        *) echo -n "$COLOR_DEFAULT" ;;
    esac
}

declare -A grid
for ((i=0; i<4; i++)); do
    for ((j=0; j<4; j++)); do
        grid[$i,$j]=0
    done
done

score=0

leaderboard_file="leaderboard.txt"

leaderboard=()
if [ -f "$leaderboard_file" ]; then
    mapfile -t leaderboard < <(sort -nr "$leaderboard_file" | head -n 10)
else
    touch "$leaderboard_file"
fi

update_leaderboard() {
    leaderboard+=("$score")
    leaderboard=($(printf "%s\n" "${leaderboard[@]}" | sort -nr))
    leaderboard=("${leaderboard[@]:0:10}")
    printf "%s\n" "${leaderboard[@]}" > "$leaderboard_file"
}

display_leaderboard() {
    echo ""
    echo "╔═════════════╗"
    echo "║   Рекорды   ║"
    echo "╠═════════════╣"
    local max_leaderboard_lines=10
    for ((k=0; k<max_leaderboard_lines; k++)); do
        if [ $k -lt ${#leaderboard[@]} ]; then
            printf "║ %2d. %5d   ║\n" "$((k +1))" "${leaderboard[$k]}"
        else
            printf "║ %2d. ------  ║\n" "$((k +1))"
        fi
    done
    echo "╚═════════════╝"
    echo ""
}

generate_new_number() {
    local empty=()
    for ((i=0; i<4; i++)); do
        for ((j=0; j<4; j++)); do
            if [ "${grid[$i,$j]}" -eq 0 ]; then
                empty+=("$i,$j")
            fi
        done
    done

    if [ ${#empty[@]} -ne 0 ]; then
        local rand_index=$((RANDOM % ${#empty[@]}))
        local pos=(${empty[$rand_index]//,/ })
        local value=$(( (RANDOM % 2 + 1) * 2 ))
        grid[${pos[0]},${pos[1]}]=$value
    fi
}

display_grid() {
    clear
    echo "╔═══════╦═══════╦═══════╦═══════╗"
    for ((i=0; i<4; i++)); do
        echo -n "║"
        for ((j=0; j<4; j++)); do
            if [ "${grid[$i,$j]}" -ne 0 ]; then
                value="${grid[$i,$j]}"
                color=$(get_color "$value")
                printf " %s%3d%s   ║" "$color" "$value" "$RESET"
            else
                printf "       ║"
            fi
        done
        echo
        if [ "$i" -lt 3 ]; then
            echo "╠═══════╬═══════╬═══════╬═══════╣"
        else
            echo "╚═══════╩═══════╩═══════╩═══════╝"
        fi
    done
    echo ""
    echo "Счет: $score"
}

shift_and_merge() {
    local -n merged_line_ref=$1
    shift
    local line=("$@")
    merged_line_ref=()

    local new_line=()
    for num in "${line[@]}"; do
        if [ "$num" -ne 0 ]; then
            new_line+=("$num")
        fi
    done

    local i=0
    while [ $i -lt ${#new_line[@]} ]; do
        if [ $((i + 1)) -lt ${#new_line[@]} ] && [ "${new_line[$i]}" -eq "${new_line[$i+1]}" ]; then
            local merged_value=$((new_line[$i] * 2))
            merged_line_ref+=("$merged_value")
            score=$((score + merged_value))
            i=$((i + 2))
        else
            merged_line_ref+=("${new_line[$i]}")
            i=$((i + 1))
        fi
    done

    while [ ${#merged_line_ref[@]} -lt 4 ]; do
        merged_line_ref+=(0)
    done
}

moved=0

move_up() {
    moved=0
    for ((j=0; j<4; j++)); do
        local line=()
        for ((i=0; i<4; i++)); do
            line+=("${grid[$i,$j]}")
        done
        shift_and_merge merged_line "${line[@]}"
        for ((i=0; i<4; i++)); do
            if [ "${grid[$i,$j]}" -ne "${merged_line[$i]}" ]; then
                moved=1
            fi
            grid[$i,$j]=${merged_line[$i]}
        done
    done
}

move_down() {
    moved=0
    for ((j=0; j<4; j++)); do
        local line=()
        for ((i=3; i>=0; i--)); do
            line+=("${grid[$i,$j]}")
        done
        shift_and_merge merged_line "${line[@]}"
        for ((i=3, k=0; i>=0; i--, k++)); do
            if [ "${grid[$i,$j]}" -ne "${merged_line[$k]}" ]; then
                moved=1
            fi
            grid[$i,$j]=${merged_line[$k]}
        done
    done
}

move_left() {
    moved=0
    for ((i=0; i<4; i++)); do
        local line=()
        for ((j=0; j<4; j++)); do
            line+=("${grid[$i,$j]}")
        done
        shift_and_merge merged_line "${line[@]}"
        for ((j=0; j<4; j++)); do
            if [ "${grid[$i,$j]}" -ne "${merged_line[$j]}" ]; then
                moved=1
            fi
            grid[$i,$j]=${merged_line[$j]}
        done
    done
}

move_right() {
    moved=0
    for ((i=0; i<4; i++)); do
        local line=()
        for ((j=3; j>=0; j--)); do
            line+=("${grid[$i,$j]}")
        done
        shift_and_merge merged_line "${line[@]}"
        for ((j=3, k=0; j>=0; j--, k++)); do
            if [ "${grid[$i,$j]}" -ne "${merged_line[$k]}" ]; then
                moved=1
            fi
            grid[$i,$j]=${merged_line[$k]}
        done
    done
}

check_game_over() {
    for ((i=0; i<4; i++)); do
        for ((j=0; j<4; j++)); do
            if [ "${grid[$i,$j]}" -eq 0 ]; then
                return 1
            fi
            if [ $i -lt 3 ] && [ "${grid[$i,$j]}" -eq "${grid[$i+1,$j]}" ]; then
                return 1
            fi
            if [ $j -lt 3 ] && [ "${grid[$i,$j]}" -eq "${grid[$i,$j+1]}" ]; then
                return 1
            fi
        done
    done
    return 0
}

generate_new_number
generate_new_number

while true; do
    display_grid
    echo "W/A/S/D для управления, Ctrl+C для выхода"

    read -n 1 -s key
    key=${key,,}

    case "$key" in
        w)
            move_up
        ;;
        s)
            move_down
        ;;
        a)
            move_left
        ;;
        d)
            move_right
        ;;
        *)
            echo "Нераспознанная клавиша: '$key'. Используйте W/A/S/D."
            continue
        ;;
    esac

    if [ "$moved" -eq 1 ]; then
        generate_new_number
    fi

    check_game_over
    if [ $? -eq 0 ]; then
        display_grid
        echo "Игра окончена! Невозможно сделать ход."
        update_leaderboard
        display_leaderboard
        echo "Ваш финальный счет: $score"
        echo "Таблица рекордов сохранена в '$leaderboard_file'."
        exit
    fi

    moved=0

done