import { mode } from "@chakra-ui/theme-tools";
export const buttonStyles = {
  components: {
    Button: {
      variants: {
        primary: {
          fontSize: "10px",
          bg: "blue.400",
          color: "#fff",
          hover: { bg: "blue.300" },
          focus: { bg: "blue.300" },
          active: { bg: "blue.300" },
        },
        navy: {
          fontSize: "10px",
          bg: "navy.900",
          color: "#fff",
          hover: { bg: "navy.900" },
          focus: { bg: "navy.900" },
          active: { bg: "navy.900" },
        },
        "no-effects": {
          hover: "none",
          active: "none",
          focus: "none",
        },
        danger: () => ({
          color: "white",
          bg: "red.500",
          fontSize: "10px",
          hover: "red.400",
          focus: "red.400",
          active: "red.400",
        }),
        outlined: (props) => ({
          color: mode("blue.400", "white")(props),
          bg: "transparent",
          fontSize: "10px",
          border: "1px solid",
          borderColor: { bg: mode("blue.400", "white")(props)},
          hover: { bg: mode("blue.50", "transparent")(props) },
          focus: { bg: mode("blue.50", "transparent")(props) },
          active: { bg: mode("blue.50", "transparent")(props) },
        }),
        dark: (props) => ({
          color: "white",
          bg: mode("gray.700", "blue.500")(props),
          fontSize: "10px",
          hover: { bg: mode("gray.700", "blue.500")(props) },
          focus: { bg: mode("gray.700", "blue.600")(props) },
          active: { bg: mode("gray.700", "blue.400")(props) },
        }),
        light: (props) => ({
          color: mode("gray.700", "gray.700")(props),
          bg: mode("gray.100", "white")(props),
          fontSize: "10px",
          hover: { bg: mode("gray.50", "white")(props) },
          focus: { bg: mode("gray.50", "white")(props) },
          active: { bg: mode("gray.50", "white")(props) },
        }),
      },
      baseStyle: {
        fontWeight: "bold",
        borderRadius: "8px",
        fontSize: "10px",
      },
    },
  },
};