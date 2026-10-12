//4x4 Matrix register  
module mreg {
    input logic                 clk,
    input logic                 rst,
    input logic                 write_en,
    input logic [1:0]           write_row,
    input logic [1:0]           write_col,
    input logic signed [7:0]    write_data,

    input logic [1:0]           read_row,
    input logic [1:0]           read_col,
    output logic signed [7:0]   read_data
};  

    logic signed [7:0] matrix [0:3][0:3];

    always_ff @(posedge clk) begin
        if (rst) begin
            for (int r = 0; r < 4;r++) begin
                for (int c = 0; c < 4; c++) begin
                    matrix[r][c] <= '0;
                end
            end
        end
        else if (write_en) begin
            matrix[write_row][write_col] <= write_data;
        end
    end

    assign read_data = matrix[read_row][read_col];

endmodule


