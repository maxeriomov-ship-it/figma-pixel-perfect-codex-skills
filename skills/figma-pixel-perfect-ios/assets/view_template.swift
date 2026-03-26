import Foundation
import SwiftUI
import UIKit

struct ConstraintBehavior {
    let pinLeft: Bool
    let pinRight: Bool
    let pinTop: Bool
    let pinBottom: Bool
    let centerX: Bool
    let centerY: Bool
    let stretchX: Bool
    let stretchY: Bool
    let fixedWidth: Bool
    let fixedHeight: Bool
    let holdLogic: String
    let axisOwnershipX: String // "parent" or "child"
    let axisOwnershipY: String // "parent" or "child"
}

struct Bounds {
    let x: CGFloat
    let y: CGFloat
    let width: CGFloat
    let height: CGFloat
}

struct TypographySpec {
    let styleName: String
    let nature: String // semantic-text / outlined-vector-text / text-inside-icon
    let fontFamily: String
    let fontFace: String
    let fontRuntimeName: String // PostScript/runtime name when applicable
    let fontAssetRef: String
    let fontFileRef: String
    let fallbackDetected: Bool
    let glyphCoverageConfirmed: Bool
    let fontSize: CGFloat
    let fontWeight: Font.Weight
    let fontStyle: String // normal / italic / oblique
    let lineHeightMode: String // px / percent / auto
    let lineHeight: CGFloat
    let letterSpacingMode: String // px / percent
    let letterSpacing: CGFloat
    let paragraphSpacing: CGFloat
    let text: String
    let textContainerWidth: CGFloat
    let textContainerHeight: CGFloat
    let lineCount: Int
    let baselineBehavior: String
}

struct CompositingSpec {
    let blendMode: String
    let localOpacity: Double
    let inheritedOpacity: Double
    let nestedOpacityFillInteractionNote: String
    let cornerSmoothing: Double?
    let effectStack: [String] // order-sensitive
}

struct AssetSource {
    let elementId: String
    let sourceType: String // figma-export / project-asset / resource-catalog
    let sourceRef: String
    let exactMatchConfirmed: Bool
    let exportabilityDecision: String // code / asset-export
}

struct PixelPerfectIOSSpec {
    let rootFrameId: String
    let width: CGFloat
    let height: CGFloat
    let paddingTop: CGFloat
    let paddingTrailing: CGFloat
    let paddingBottom: CGFloat
    let paddingLeading: CGFloat
    let gap: CGFloat
    let constraint: ConstraintBehavior
    let visualBounds: Bounds
    let hitAreaBounds: Bounds
    let subpixelPlacementAllowed: Bool
    let typography: TypographySpec
    let compositing: CompositingSpec
    let assetSources: [AssetSource]
    let repeatedInstancesConfirmed: Bool
    let feasibilityRisks: [String]
    let negativeSpaceProtected: Bool
    let fontRegistrationConfirmed: Bool
}

func assertConfirmed(_ condition: @autoclosure () -> Bool, _ message: String) {
    if !condition() {
        fatalError("Unconfirmed critical parameter: \(message)")
    }
}

struct PixelPerfectSwiftUIView: View {
    let spec: PixelPerfectIOSSpec

    var body: some View {
        let _ = Self.validate(spec)

        VStack(alignment: .leading, spacing: spec.gap) {
            if spec.typography.nature == "semantic-text" {
                Text(spec.typography.text)
                    .font(.custom(spec.typography.fontRuntimeName, size: spec.typography.fontSize))
                    .fontWeight(spec.typography.fontWeight)
                    .lineSpacing(max(spec.typography.lineHeight - spec.typography.fontSize, 0))
                    .tracking(spec.typography.letterSpacing)
                    .frame(width: spec.typography.textContainerWidth,
                           height: spec.typography.textContainerHeight,
                           alignment: .leading)
                    .lineLimit(spec.typography.lineCount)
                    .alignmentGuide(.firstTextBaseline) { d in d[.firstTextBaseline] }
            } else {
                Color.clear
                    .overlay(Text("Vector/graphic text must come from exact source asset"))
            }
        }
        .padding(.top, spec.paddingTop)
        .padding(.trailing, spec.paddingTrailing)
        .padding(.bottom, spec.paddingBottom)
        .padding(.leading, spec.paddingLeading)
        .frame(width: spec.width, height: spec.height, alignment: .topLeading)
        .contentShape(Rectangle())
    }

    static func validate(_ spec: PixelPerfectIOSSpec) {
        assertConfirmed(!spec.rootFrameId.isEmpty, "rootFrameId")
        assertConfirmed(spec.paddingTop >= 0, "paddingTop")
        assertConfirmed(spec.paddingTrailing >= 0, "paddingTrailing")
        assertConfirmed(spec.paddingBottom >= 0, "paddingBottom")
        assertConfirmed(spec.paddingLeading >= 0, "paddingLeading")
        assertConfirmed(!spec.constraint.holdLogic.isEmpty, "constraint.holdLogic")
        assertConfirmed(!spec.typography.styleName.isEmpty, "typography.styleName")
        assertConfirmed(!spec.typography.fontFamily.isEmpty, "typography.fontFamily")
        assertConfirmed(!spec.typography.fontFace.isEmpty, "typography.fontFace")
        assertConfirmed(!spec.typography.fontRuntimeName.isEmpty, "typography.fontRuntimeName")
        assertConfirmed(!spec.typography.fontAssetRef.isEmpty, "typography.fontAssetRef")
        assertConfirmed(!spec.typography.fontFileRef.isEmpty, "typography.fontFileRef")
        assertConfirmed(!spec.typography.baselineBehavior.isEmpty, "typography.baselineBehavior")
        assertConfirmed(spec.fontRegistrationConfirmed, "fontRegistrationConfirmed")
        assertConfirmed(!spec.typography.fallbackDetected, "runtime font fallback detected")
        assertConfirmed(spec.typography.glyphCoverageConfirmed, "glyph coverage not confirmed")
        assertConfirmed(spec.repeatedInstancesConfirmed, "repeated instance consistency")
        assertConfirmed(spec.assetSources.allSatisfy { $0.exactMatchConfirmed }, "asset source-of-truth mismatch")
        assertConfirmed(spec.negativeSpaceProtected, "negative space protection")
    }
}

final class PixelPerfectUIKitView: UIView {
    private let label = UILabel()

    init(spec: PixelPerfectIOSSpec) {
        super.init(frame: .zero)
        translatesAutoresizingMaskIntoConstraints = false

        PixelPerfectSwiftUIView.validate(spec)

        label.translatesAutoresizingMaskIntoConstraints = false
        label.text = spec.typography.text
        label.numberOfLines = spec.typography.lineCount
        label.font = UIFont(name: spec.typography.fontRuntimeName, size: spec.typography.fontSize)

        addSubview(label)

        NSLayoutConstraint.activate([
            widthAnchor.constraint(equalToConstant: spec.width),
            heightAnchor.constraint(equalToConstant: spec.height),

            label.topAnchor.constraint(equalTo: topAnchor, constant: spec.paddingTop),
            label.leadingAnchor.constraint(equalTo: leadingAnchor, constant: spec.paddingLeading),
            label.trailingAnchor.constraint(lessThanOrEqualTo: trailingAnchor, constant: -spec.paddingTrailing),
            label.bottomAnchor.constraint(lessThanOrEqualTo: bottomAnchor, constant: -spec.paddingBottom),
            label.widthAnchor.constraint(equalToConstant: spec.typography.textContainerWidth)
        ])
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
