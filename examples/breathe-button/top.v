/*
 *	Copyright (c) 2024, Signaloid.
 *
 *	Permission is hereby granted, free of charge, to any person obtaining a copy
 *	of this software and associated documentation files (the "Software"), to deal
 *	in the Software without restriction, including without limitation the rights
 *	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *	copies of the Software, and to permit persons to whom the Software is
 *	furnished to do so, subject to the following conditions:
 *
 *	The above copyright notice and this permission notice shall be included in all
 *	copies or substantial portions of the Software.
 *
 *	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 *	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 *	SOFTWARE.
 */

module top 
(
	input	SD_DAT2,
	input	SD_DAT3,
	output	LED_GREEN,
	output	LED_RED
);

	/*
	 *	Creates a 24MHz clock signal from
	 *	internal oscillator of the iCE40
	 */

	wire clk;
	SB_HFOSC #(.CLKHF_DIV ("0b01")) OSCInst0 (
		.CLKHFEN(1'b1),
		.CLKHFPU(1'b1),
		.CLKHF(clk)
	);

	reg [2:0] clk_div;
	always @(posedge clk ) begin
		clk_div <= clk_div + 1;
	end

	reg [7:0] led_ip_data = 0;
	reg [3:0] led_ip_addr = 0;
	reg led_ip_den = 0;
	reg led_ip_exe = 0;

	wire rgb_pwm_ip_out_0;
	wire rgb_pwm_ip_out_1;

	SB_LEDDA_IP PWMgen_inst (
		.LEDDCS(1'b1),
		.LEDDCLK(clk),
		.LEDDDAT7(led_ip_data[7]),
		.LEDDDAT6(led_ip_data[6]),
		.LEDDDAT5(led_ip_data[5]),
		.LEDDDAT4(led_ip_data[4]),
		.LEDDDAT3(led_ip_data[3]),
		.LEDDDAT2(led_ip_data[2]),
		.LEDDDAT1(led_ip_data[1]),
		.LEDDDAT0(led_ip_data[0]),
		.LEDDADDR3(led_ip_addr[3]),
		.LEDDADDR2(led_ip_addr[2]),
		.LEDDADDR1(led_ip_addr[1]),
		.LEDDADDR0(led_ip_addr[0]),
		.LEDDDEN(led_ip_den),
		.LEDDEXE(led_ip_exe),
		.PWMOUT0(rgb_pwm_ip_out_0), 
		.PWMOUT1(rgb_pwm_ip_out_1)
	);

	reg [7:0] 	wait_clock = 0;
	reg [4:0]	init_stack_pointer;
	wire [11:0]	init_stack [7:0];
	wire [3:0]	init_register_addr = init_stack[init_stack_pointer][3:0];
	wire [7:0]	init_register_data = init_stack[init_stack_pointer][11:4];
	reg [2:0]	breathe_rate_register = 0;

	/*
	 *	Register addresses for SB_LEDDA_IP block
	 */
	localparam k_LEDDCR0_Addr 	= 4'b1000;
	localparam k_LEDDBR_Addr 	= 4'b1001;
	localparam k_LEDDONR_Addr 	= 4'b1010;
	localparam k_LEDDOFR_Addr 	= 4'b1011;
	localparam k_LEDDBCRR_Addr 	= 4'b0101;
	localparam k_LEDDBCFR_Addr 	= 4'b0110;
	localparam k_LEDDPWRR_Addr 	= 4'b0001;
	localparam k_LEDDPWRG_Addr 	= 4'b0010;
	
	/*
	 *	Stack of init values for SB_LEDDA_IP registers
	 */
	assign init_stack[00] = {8'b11001001, k_LEDDCR0_Addr}; 		/* LEDDCR0 */
	assign init_stack[01] = {8'b01110110, k_LEDDBR_Addr};		/* LEDDBR */
	assign init_stack[02] = {8'b00000100, k_LEDDONR_Addr};		/* LEDDONR */
	assign init_stack[03] = {8'b00000100, k_LEDDOFR_Addr};		/* LEDDOFR */
	assign init_stack[04] = {8'b11000011, k_LEDDBCRR_Addr};		/* LEDDBCRR */
	assign init_stack[05] = {8'b11000011, k_LEDDBCFR_Addr};		/* LEDDBCFR */
	assign init_stack[06] = {8'b11111111, k_LEDDPWRR_Addr};		/* LEDDPWRR */
	assign init_stack[07] = {8'b11111111, k_LEDDPWRG_Addr};		/* LEDDPWRG */

	wire button_a_debounced;
	wire button_b_debounced;

	debounce  debounce_inst_1 (
		.clk(clk),
		.button_in(!SD_DAT2),
		.button_out(button_a_debounced)
	);

	debounce  debounce_inst_2 (
		.clk(clk),
		.button_in(!SD_DAT3),
		.button_out(button_b_debounced)
	);

	localparam kFSMStateInit = 0;
	localparam kFSMStateWaitButton = 1;
	localparam kFSMStateUpdateLEDDBCRR = 2;
	localparam kFSMStateUpdateLEDDBCFR = 3;
	localparam kFSMStateWaitButtonDisengage = 4;

	reg [3:0]  fsm_state = kFSMStateInit;

	always @(posedge clk_div[2]) begin
		led_ip_exe <= 1'b0;
		case (fsm_state)
			kFSMStateInit: begin
				/*
				 *	Initialize breath rate register
				 */
				breathe_rate_register <= 3'b010;

				/*
				 *	Initialize registers of SB_LEDDA_IP
				 */
				led_ip_addr <= init_register_addr;
				led_ip_data <= init_register_data;
				led_ip_den <= 1'b1;
				if (led_ip_den) begin
					led_ip_den <= 1'b0;
					init_stack_pointer <= init_stack_pointer + 1;
					if (init_stack_pointer == 7) begin
						/*
						 *	Start LED breathing
						 */
						led_ip_den <= 1'b0;
						fsm_state <= kFSMStateWaitButton;
					end
				end
			end
			kFSMStateWaitButton: begin
				/*
				 *	Wait for button press to increase breathe ramp time
				 */
				led_ip_exe <= 1'b1;
				if(button_a_debounced && (breathe_rate_register != 3'b111)) begin
					breathe_rate_register <= breathe_rate_register + 1;
					led_ip_exe <= 1'b0;
					fsm_state <= kFSMStateUpdateLEDDBCRR;
				end
				/*
				 *	Wait for button press to decrease breathe ramp time
				 */
				else if(button_b_debounced && (breathe_rate_register != 0)) begin
					breathe_rate_register <= breathe_rate_register - 1;
					led_ip_exe <= 1'b0;
					fsm_state <= kFSMStateUpdateLEDDBCRR;
				end
			end
			kFSMStateUpdateLEDDBCRR: begin
				/*
				 *	Update LEDDBCRR register
				 */
				led_ip_addr <= k_LEDDBCRR_Addr;
				led_ip_data <= {5'b11000, breathe_rate_register};
				led_ip_den <= 1'b1;
				if (led_ip_den) begin
					led_ip_den <= 1'b0;
					fsm_state <= kFSMStateUpdateLEDDBCFR;
				end
			end
			kFSMStateUpdateLEDDBCFR: begin
				/*
				 *	Update LEDDBCFR register
				 */
				led_ip_addr <= k_LEDDBCFR_Addr;
				led_ip_data <= {5'b11000, breathe_rate_register};
				led_ip_den <= 1'b1;
				if (led_ip_den) begin
					led_ip_den <= 1'b0;
					fsm_state <= kFSMStateWaitButtonDisengage;
				end
			end
			kFSMStateWaitButtonDisengage: begin
				led_ip_exe <= 1'b1;
				if (!(button_a_debounced || button_b_debounced)) begin
					fsm_state <= kFSMStateWaitButton;
				end
			end
		endcase
	end

	wire rgb_pwm_0;
	wire rgb_pwm_1;

	SB_RGBA_DRV #(
		.CURRENT_MODE("0b1"),
		.RGB0_CURRENT("0b000001"),
		.RGB1_CURRENT("0b000001")
	)
	RGBA_DRIVER (
		.CURREN(1'b1),
		.RGBLEDEN(1'b1),
		.RGB0PWM(rgb_pwm_0),
		.RGB1PWM(rgb_pwm_1),
		.RGB0(LED_RED),
		.RGB1(LED_GREEN)
	);

	assign rgb_pwm_0 = rgb_pwm_ip_out_0;
	assign rgb_pwm_1 = !rgb_pwm_ip_out_1;


endmodule
 