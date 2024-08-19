# SolidKey-1-Keyboard-PCB
A capacitive touch QMK keyboard, with aspirations of replacing the Framework 13 keyboard

## Inspiration

* This project is inspired by [ebastler's UnMechanical Keyboard](https://github.com/ebastler/UnMechanical).

## Goals

* Make a columnar keyboard with a capacitive touch interface.
* Make the keyboard fit between the Framework 13 keyboard space and screen. Be compatible with the Framework 13 input cover's wiring.
* Base the locations of the keys on the Iris 6 keyboard.
* Parts:
    * RP2040 microcontroller
    * USB-C
    * Vibration motor
    * No LEDs!
* Low-ish power, low mass
* <$80 for a fully-assembled keyboard from JLCPCB

## Licence

The hardware component of this project is licenced under the `CERN Open Hardware Licence Version 2 - Weakly Reciprocal` licence. Variations must be shared under the same licence (or equivalent) licence. Commercial use is allowed, but the source must be shared, and it must be released/sold under a different name.

## Notes

* Framework 13 keyboard dimensions: 276.76mm x 105.0mm x 1.74mm, at the bottom of the taper up, based on their full STEP CAD model.
* For the 276mm x 105mm PCB from JLCPCB, it costs:
    * US$16.80 for 0.6mm thick, LeadFree HASL
    * US$60.60 for 0.4mm thick, requiring ENIG
    * US$10 shipping for these thin boards.
    * US$50 for 0.6mm assembly ("Standard"), but US$26 for 0.8mm assembly ("Economic").
    * 0.8mm weighs 54g each. 0.6mm weighs 40g-54g each.

## Resources

* RP2040 Design Guide: https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf
* CY8CMBR3116 Capacitive Touch Guides:
    * Datasheet: https://www.infineon.com/cms/en/product/microcontroller/sensing-controller/capsense-controllers/capsense-mbr3/cy8cmbr3116-lqxit/
    * CY8CMBR3xxx CapSense Design Guide: https://www.cypress.com/?rID=90800
    * Getting Started with CapSense: https://www.cypress.com/?rID=48787

## Future Work

* Add a dot mouse thing, like the ThinkPad keyboards.
