

ZSTD_COMP_total_uncompressed = 0
ZSTD_COMP_total_compressed = 0
ZSTD_COMP_total_time_s = 0

with open('intermediates/XEON_ZSTD_COMPRESS_RESULT', 'r') as xeon_data:
    f = xeon_data.readlines()

    for line in f:
        if line.startswith("zstd 1.5.2"):
            l = line.split(",")
            compression_MBps = float(l[1])
            uncompressed_size = float(l[3])
            compressed_size = float(l[4])

            compression_Bps = compression_MBps * 1000000.0

            time_s = uncompressed_size / compression_Bps

            ZSTD_COMP_total_time_s += time_s
            ZSTD_COMP_total_uncompressed += uncompressed_size
            ZSTD_COMP_total_compressed += compressed_size

ZSTD_DECOMP_total_uncompressed = 0
ZSTD_DECOMP_total_compressed = 0
ZSTD_DECOMP_total_time_s = 0

with open('intermediates/XEON_ZSTD_DECOMPRESS_RESULT', 'r') as xeon_data:
    f = xeon_data.readlines()

    for line in f:
        if line.startswith("zstd 1.5.2"):
            l = line.split(",")
            decompression_MBps = float(l[2])
            uncompressed_size = float(l[3])
            compressed_size = float(l[4])

            decompression_Bps = decompression_MBps * 1000000.0

            time_s = uncompressed_size / decompression_Bps

            ZSTD_DECOMP_total_time_s += time_s
            ZSTD_DECOMP_total_uncompressed += uncompressed_size
            ZSTD_DECOMP_total_compressed += compressed_size

print("OPERATION,uncomp_data_size,comp_data_size,time_s")
print(f"COMPRESS,{ZSTD_COMP_total_uncompressed},{ZSTD_COMP_total_compressed},{ZSTD_COMP_total_time_s}")
print(f"DECOMPRESS,{ZSTD_DECOMP_total_uncompressed},{ZSTD_DECOMP_total_compressed},{ZSTD_DECOMP_total_time_s}")
