.data
.align 3
const_0: .double 7.5
const_1: .double 2.5
const_2: .double 20.0
const_3: .double 8.0
const_4: .double 2.0
const_5: .double 3.0
const_6: .double 4.0
const_7: .double 16.0
const_8: .double 17.0
const_9: .double 8.5
const_10: .double 1.5
const_11: .double 1.0
mem_slot: .double 0.0
var_VAR: .double 0.0
result_0: .double 0.0
result_1: .double 0.0
result_2: .double 0.0
result_3: .double 0.0
result_4: .double 0.0
result_5: .double 0.0
result_6: .double 0.0
result_7: .double 0.0
result_8: .double 0.0
result_9: .double 0.0
result_10: .double 0.0
result_11: .double 0.0

.text
.global _start
_start:
    @ --- expressao 0 ---
    LDR r0, =const_0
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_1
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VADD.F64 d0, d1, d0
    LDR r0, =result_0
    VSTR.F64 d0, [r0]

    @ --- expressao 1 ---
    LDR r0, =const_2
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_3
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VSUB.F64 d0, d1, d0
    LDR r0, =result_1
    VSTR.F64 d0, [r0]

    @ --- expressao 2 ---
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VADD.F64 d0, d1, d0
    VPUSH {d0}
    LDR r0, =const_6
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VMUL.F64 d0, d1, d0
    LDR r0, =result_2
    VSTR.F64 d0, [r0]

    @ --- expressao 3 ---
    LDR r0, =const_7
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_6
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VDIV.F64 d0, d1, d0
    VPUSH {d0}
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VADD.F64 d0, d1, d0
    LDR r0, =result_3
    VSTR.F64 d0, [r0]

    @ --- expressao 4 ---
    LDR r0, =const_8
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VPOP {d1}
    BL div_int_double
    LDR r0, =result_4
    VSTR.F64 d0, [r0]

    @ --- expressao 5 ---
    LDR r0, =const_8
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VPOP {d1}
    BL mod_int_double
    LDR r0, =result_5
    VSTR.F64 d0, [r0]

    @ --- expressao 6 ---
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VPOP {d1}
    BL pow_int_double
    LDR r0, =result_6
    VSTR.F64 d0, [r0]

    @ --- expressao 7 ---
    LDR r0, =const_9
    VLDR.F64 d0, [r0]
    LDR r0, =var_VAR
    VSTR.F64 d0, [r0]
    LDR r0, =result_7
    VSTR.F64 d0, [r0]

    @ --- expressao 8 ---
    LDR r0, =var_VAR
    VLDR.F64 d0, [r0]
    LDR r0, =result_8
    VSTR.F64 d0, [r0]

    @ --- expressao 9 ---
    LDR r0, =var_VAR
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_10
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VADD.F64 d0, d1, d0
    VPUSH {d0}
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VMUL.F64 d0, d1, d0
    VPOP {d1}
    VDIV.F64 d0, d1, d0
    LDR r0, =result_9
    VSTR.F64 d0, [r0]

    @ --- expressao 10 ---
    LDR r0, =result_8
    VLDR.F64 d0, [r0]
    LDR r0, =result_10
    VSTR.F64 d0, [r0]

    @ --- expressao 11 ---
    LDR r0, =const_11
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VADD.F64 d0, d1, d0
    VPUSH {d0}
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VPUSH {d0}
    LDR r0, =const_6
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VADD.F64 d0, d1, d0
    VPOP {d1}
    VMUL.F64 d0, d1, d0
    VPUSH {d0}
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VPOP {d1}
    VDIV.F64 d0, d1, d0
    LDR r0, =result_11
    VSTR.F64 d0, [r0]

    @ --- exibe ultimo resultado nos LEDs ---
    LDR r0, =result_11
    VLDR.F64 d0, [r0]
    VCVT.S32.F64 s0, d0
    VMOV r1, s0
    LDR r0, =0xFF200000
    STR r1, [r0]

fim:
    B fim

@ sdiv_software: r1 / r0 -> quociente em r2, resto em r3
@ nao salva lr pois e chamado por div_int_double e mod_int_double
sdiv_software:
    MOV r2, #0
sdiv_loop:
    CMP r1, r0
    BLT sdiv_fim
    SUB r1, r1, r0
    ADD r2, r2, #1
    B sdiv_loop
sdiv_fim:
    MOV r3, r1
    BX lr

div_int_double:
    PUSH {lr}
    VCVT.S32.F64 s2, d1
    VCVT.S32.F64 s0, d0
    VMOV r1, s2
    VMOV r0, s0
    BL sdiv_software
    VMOV s0, r2
    VCVT.F64.S32 d0, s0
    POP {lr}
    BX lr

mod_int_double:
    PUSH {lr}
    VCVT.S32.F64 s2, d1
    VCVT.S32.F64 s0, d0
    VMOV r1, s2
    VMOV r0, s0
    BL sdiv_software
    VMOV s0, r3
    VCVT.F64.S32 d0, s0
    POP {lr}
    BX lr

pow_int_double:
    PUSH {lr}
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    VMOV.F64 d2, #1.0
pow_loop:
    CMP r0, #0
    BEQ pow_fim
    VMUL.F64 d2, d2, d1
    SUB r0, r0, #1
    B pow_loop
pow_fim:
    VMOV.F64 d0, d2
    POP {lr}
    BX lr