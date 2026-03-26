import SwiftUI

struct FigmaTokenAlias {
    let aliasPath: String
    let resolvedPath: String
    let resolvedValueDescription: String
}

enum FigmaColorToken {
    static let background = Color(red: 0.0, green: 0.0, blue: 0.0)
    static let foreground = Color(red: 1.0, green: 1.0, blue: 1.0)

    static let backgroundAlias = FigmaTokenAlias(
        aliasPath: "color/background/default",
        resolvedPath: "color/neutral/1000",
        resolvedValueDescription: "#000000"
    )
}

enum FigmaTypographyToken {
    static let styleName = "REPLACE_WITH_FIGMA_TEXT_STYLE"
    static let fontFamily = "REPLACE_WITH_EXACT_FIGMA_FAMILY"
    static let fontFace = "REPLACE_WITH_EXACT_FIGMA_FACE"
    static let fontRuntimeName = "REPLACE_WITH_EXACT_RUNTIME_OR_POSTSCRIPT_NAME"
    static let fontAssetRef = "REPLACE_WITH_FONT_ASSET_KEY"
    static let fontFileRef = "REPLACE_WITH_FONT_FILE"
    static let sourceType = "project-local|package|platform"

    static let fontSize: CGFloat = 0
    static let fontWeight: CGFloat = 400
    static let fontStyle = "normal"
    static let lineHeightMode = "px"
    static let lineHeight: CGFloat = 0
    static let letterSpacingMode = "px"
    static let letterSpacing: CGFloat = 0
    static let paragraphSpacing: CGFloat = 0
    static let textTransform = "none"
    static let textDecoration = "none"

    static let axisWght: CGFloat? = nil
    static let axisOpsz: CGFloat? = nil

    static let fallbackDetectionRequired = true
    static let runtimeRegistrationRequired = true
}

enum FigmaSpacingToken {
    static let top: CGFloat = 0
    static let right: CGFloat = 0
    static let bottom: CGFloat = 0
    static let left: CGFloat = 0
    static let gap: CGFloat = 0
}

enum FigmaVisualToken {
    static let borderWidth: CGFloat = 0
    static let hairlineWidth: CGFloat = 0.5
    static let cornerRadius: CGFloat = 0
    static let cornerSmoothing: CGFloat = 0
    static let blendMode: String = "normal"
    static let effectStackOrder: [String] = ["shadow1", "shadow2", "stroke", "blur"]
}

// Guard:
// 1) resolve alias chain before use,
// 2) map exact face to exact runtime name,
// 3) confirm registration/runtime usage,
// 4) do not silently replace with system fallback.
