#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>

#define mem_size 64
#define cache_size 8
#define set_size 2
#define set_count (cache_size / set_size)

// Tag Arrays
static int16_t set_1_tags[set_count];
static int16_t set_2_tags[set_count];

// Data Arrays
static int16_t set_1_data[set_count];
static int16_t set_2_data[set_count];

// FIFO Check Array
static uint8_t last_used[set_count];

// Memory Table
static uint8_t memory[mem_size] = {
    0x92,
    0x70,
    0x8C,
    0xFD,
    0xB9,
    0xE2,
    0x40,
    0xC2,
    0x0D,
    0x9A,
    0xD1,
    0xF8,
    0x43,
    0x7E,
    0xB7,
    0x75,
    0xFB,
    0x44,
    0xDD,
    0xF6,
    0xA6,
    0x43,
    0x11,
    0x17,
    0x98,
    0x88,
    0x08,
    0x6A,
    0x6D,
    0xB8,
    0xBC,
    0x12,
    0x0A,
    0xF1,
    0x4C,
    0x45,
    0x63,
    0x2C,
    0x40,
    0x98,
    0x91,
    0x65,
    0x0E,
    0x76,
    0xEE,
    0x5D,
    0x18,
    0x29,
    0x85,
    0x13,
    0x60,
    0xC5,
    0x56,
    0xF2,
    0x89,
    0x9E,
    0x06,
    0xE2,
    0x0B,
    0xA2,
    0xB2,
    0x41,
    0xB1,
    0x7B
};

int main(void) {
    uint8_t address;
    uint8_t tag;
    uint8_t set;

    // Initialize last used array to 2
    memset(last_used, 2, set_count);

    printf("Please enter a valid 2 digit (decimal) address (0-63) or Ctrl + C to quit.\n\n");
    scanf("%" SCNu8, &address);

    while (1) {
        tag = address >> 2; // Bits [5..2]
        set = address & 3;  // Bits [1..0]
        
        if (address > 63) {
            printf("\nMust be between 0-63.\n\n");
        } else if (set_1_tags[set] == tag && set_1_data[set] == memory[address]) {
            printf("\nCache hit!\n\n");
            printf("Data at %02d: %02X\n\n", address, memory[address]);
        } else if (set_2_tags[set] == tag && set_2_data[set] == memory[address]) {
            printf("\nCache hit!\n\n");
            printf("Data at %02d: %02X\n\n", address, memory[address]);
        } else {
            if (last_used[set] == 1) {
                set_2_tags[set] = tag;
                set_2_data[set] = memory[address];
                last_used[set] = 2;
            } else {
                set_1_tags[set] = tag;
                set_1_data[set] = memory[address];
                last_used[set] = 1;
            }
            printf("\nCache miss.\n\n");
        }

        printf("Set  Tag   Data  Tag   Data\n");
        for (uint8_t i = 0; i < 4; i++) {
            printf(" %d    %02d    %02X    %02d    %02X\n", i, set_1_tags[i], set_1_data[i], set_2_tags[i], set_2_data[i]);
        }

        printf("\nPlease enter a valid 2 digit (decimal) address (0-63) or Ctrl + C to quit.\n\n");
        scanf("%" SCNu8, &address);
    }
}