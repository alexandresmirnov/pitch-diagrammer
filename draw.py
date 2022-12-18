import math
import cairo
import xml.etree.ElementTree as ET
import argparse


def generate_svg(
    pitch_pattern: str,
    text_string: str,
    height: float,
    step: float,
    padding: float,
    outer_point_radius: float,
    inner_point_radius: float,
    output_file: str,
) -> None:

    edge_offset = outer_point_radius + padding

    width = ((len(pitch_pattern) - 1) * step) + (outer_point_radius * 2) + (padding * 2)

    points: tuple[float, float] = []

    for i, char in enumerate(pitch_pattern):
        curr_x = edge_offset + (step * i)
        curr_y = edge_offset if char == "H" else height - edge_offset

        points.append((curr_x, curr_y))

    print(points)

    with cairo.SVGSurface(output_file, width, height) as surface:
        context = cairo.Context(surface)

        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.set_line_width(1)

        context.set_source_rgba(0, 0, 0, 1)

        # punch out each point into the clip area
        for x, y in points:
            context.arc(x, y, outer_point_radius, 0, 2 * math.pi)
            context.new_sub_path()

        # draw big rectangle around whole area
        context.move_to(0, 0)
        context.line_to(0, height)
        context.line_to(width, height)
        context.line_to(width, 0)
        context.close_path()

        # clip area between punched-out circles and outer edges
        context.clip()

        # start drawing actual diagram
        context.set_source_rgba(0, 0, 0, 1)
        context.set_line_width(10)

        # draw lines
        context.new_sub_path()
        for x, y in points:
            context.line_to(x, y)

        context.stroke()

        # now draw each actual point
        for x, y in points:
            context.arc(x, y, inner_point_radius + 2, 0, 2 * math.pi)
            context.stroke()

    # now add text
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(output_file)
    root = tree.getroot()

    for i, (x, y) in enumerate(points):
        letter = text_string[i]

        font_size = inner_point_radius * 1.3

        text_element = ET.Element(
            "text",
            attrib={
                "x": f"{x}",
                "y": f"{y}",
                "style": f"font-size: {font_size}px; dominant-baseline: middle; text-anchor:middle",
            },
        )
        text_element.text = letter
        root.append(text_element)

    tree.write(output_file)


def main():
    parser = argparse.ArgumentParser(
        prog="Pitch Diagrammer",
        description="Generate an SVG of a pitch diagram with specified parameters",
    )

    parser.add_argument("--pitch_pattern", type=str)
    parser.add_argument("--text_string", type=str)
    parser.add_argument("--height", type=float, default=150)
    parser.add_argument("--step", type=float, default=100)
    parser.add_argument("--padding", type=float, default=10)
    parser.add_argument("--outer_point_radius", type=float, default=10)
    parser.add_argument("--inner_point_radius", type=float, default=8)
    parser.add_argument("--output_file", type=str, default="output.svg")
    args = parser.parse_args()

    generate_svg(
        pitch_pattern=args.pitch_pattern,
        text_string=args.text_string,
        height=args.height,
        step=args.step,
        padding=args.padding,
        outer_point_radius=args.outer_point_radius,
        inner_point_radius=args.inner_point_radius,
        output_file=args.output_file,
    )


if __name__ == "__main__":
    main()
