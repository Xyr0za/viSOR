def dump_csv(file_name: str, parser: object):
    X = parser.X
    Y = parser.Y

    with open(file_name, 'w', newline='') as csvfile:
        csvfile.write(",0,Distance,Backscatter\n")

        import time

        # Simulated input data (replace this with your actual list of dicts)
        data = parser.raw

        def get_section(name):
            try:
                return next((item for item in data if item.get('name') == name), {})
            except Exception:
                return {}

        def safe_get(func):
            try:
                return func()
            except Exception:
                return ""

        # Sections
        fxd = get_section('FxdParams')
        sup = get_section('SupParams')

        # Extracted fields with protection
        scaling_factor = safe_get(lambda: "1.0")
        averaging_time = safe_get(lambda: f"{fxd['averaging_time']} sec")
        date_epoch = safe_get(lambda: fxd['date_time'])
        date_str = safe_get(
            lambda: f"{time.strftime('%a %b %d %H:%M:%S %Y', time.localtime(date_epoch))} ({date_epoch} sec)")
        ref_index = safe_get(lambda: f"{fxd['index_of_refraction']:.6f}")
        num_averages = safe_get(lambda: fxd['number_of_averages'])
        pulse_width = safe_get(lambda: f"{fxd['pulse_width']} ns")
        range_val = safe_get(lambda: f"{fxd['acquisition_range_distance']:.12f}")
        resolution = safe_get(lambda: f"{(1 / fxd['sample_spacing']) * 2e8 * 1e-3:.14f}")
        units = safe_get(lambda: "mt (meters)")
        module = safe_get(lambda: sup['module_name'])
        otdr = safe_get(lambda: sup['otdr_name'])
        software = safe_get(lambda: sup['software_version'])

        # Output
        # Inside: with open("output.csv", "w") as file:

        csvfile.write(f"full file,{file_name}\n")
        csvfile.write(f"scaling factor,{scaling_factor}\n")
        csvfile.write(f"averaging time,{averaging_time}\n")
        csvfile.write(f"date/time,{date_str}\n")
        csvfile.write(f"Ref Index,{ref_index}\n")
        csvfile.write(f"num averages,{num_averages}\n")
        csvfile.write(f"pulse width,{pulse_width}\n")
        csvfile.write(f"range,{range_val}\n")
        csvfile.write(f"resolution,{resolution}\n")
        csvfile.write(f"units,{units}\n")
        csvfile.write(f"module,{module}\n")
        csvfile.write(f"OTDR,{otdr}\n")
        csvfile.write(f"software,{software}\n")

        for i, (x, y) in enumerate(zip(X, Y)):
            csvfile.write(f"{i},,{round(x, 5)},{round(y, 5)}\n")


def dump_tsv(file_name: str, parser: object):
    X = parser.X
    Y = parser.Y

    with open(file_name, 'w', newline='') as csvfile:
        for x, y in zip(X, Y):
            csvfile.write(f",,{x}\t{y}\n")
