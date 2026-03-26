import React from "react";

type Px = number;

type Bounds = {
  x: Px;
  y: Px;
  width: Px;
  height: Px;
};

type ConstraintBehavior = {
  pinLeft: boolean;
  pinRight: boolean;
  pinTop: boolean;
  pinBottom: boolean;
  centerX: boolean;
  centerY: boolean;
  stretchX: boolean;
  stretchY: boolean;
  fixedWidth: boolean;
  fixedHeight: boolean;
  holdLogic: string;
  axisOwnership: {
    x: "parent" | "child";
    y: "parent" | "child";
  };
};

type TextLayerNature = "semantic-text" | "outlined-vector-text" | "text-inside-icon";

type TypographySpec = {
  styleName: string;
  nature: TextLayerNature;
  fontFamily: string;
  fontFace: string;
  fontAssetRef: string;
  fontFileRef: string;
  fallbackDetected: boolean;
  glyphCoverageConfirmed: boolean;
  fontSize: Px;
  fontWeight: number;
  fontStyle: "normal" | "italic" | "oblique";
  lineHeightMode: "px" | "percent" | "auto";
  lineHeight: Px;
  letterSpacingMode: "px" | "percent";
  letterSpacing: Px;
  paragraphSpacing: Px;
  textDecoration: "none" | "underline" | "line-through" | "overline";
  textAlign: "left" | "center" | "right" | "justify";
  textTransform: "none" | "uppercase" | "lowercase" | "capitalize";
  textCase: "original" | "upper" | "lower" | "title";
  wrappingBehavior: "pre-wrap" | "nowrap" | "normal";
  textValue: string;
  textContainerWidth: Px;
  textContainerHeight: Px;
  lineCount: number;
  baselineBehavior: string;
  variableAxes?: Record<string, number>;
};

type CompositingSpec = {
  blendMode: "normal" | "multiply" | "overlay" | "screen" | "darken" | "lighten" | "other";
  localOpacity: number;
  inheritedOpacity: number;
  nestedOpacityFillInteractionNote: string;
  cornerSmoothing: number | null;
  effectStack: Array<{
    order: number;
    kind: "shadow" | "inner-shadow" | "stroke" | "blur" | "other";
    value: string;
  }>;
};

type AssetSource = {
  elementId: string;
  sourceType: "figma-export" | "project-asset" | "resource-catalog";
  sourceRef: string;
  exactMatchConfirmed: boolean;
  exportabilityDecision: "code" | "asset-export";
};

type PixelPerfectWebSpec = {
  rootFrameId: string;
  layout: {
    width: Px;
    height: Px;
    paddingTop: Px;
    paddingRight: Px;
    paddingBottom: Px;
    paddingLeft: Px;
    marginTop: Px;
    marginRight: Px;
    marginBottom: Px;
    marginLeft: Px;
    gap: Px;
    intrinsicSpacingConfirmed: boolean;
    accidentalGapRejected: boolean;
    negativeSpaceProtected: boolean;
    constraint: ConstraintBehavior;
  };
  visualBounds: Bounds;
  hitAreaBounds: Bounds;
  subpixelPlacementAllowed: boolean;
  compositing: CompositingSpec;
  typography: TypographySpec;
  assetSources: AssetSource[];
  repeatedInstanceGroup: {
    groupId: string;
    allInstancesConfirmedIdentical: boolean;
  };
  feasibilityRisks: string[];
};

function assertConfirmed(value: unknown, label: string): void {
  if (value === null || value === undefined || value === "") {
    throw new Error(`Unconfirmed critical parameter: ${label}`);
  }
}

function assertStrict(spec: PixelPerfectWebSpec): void {
  assertConfirmed(spec.rootFrameId, "rootFrameId");
  assertConfirmed(spec.layout.width, "layout.width");
  assertConfirmed(spec.layout.paddingTop, "layout.paddingTop");
  assertConfirmed(spec.layout.paddingRight, "layout.paddingRight");
  assertConfirmed(spec.layout.paddingBottom, "layout.paddingBottom");
  assertConfirmed(spec.layout.paddingLeft, "layout.paddingLeft");
  assertConfirmed(spec.layout.constraint.holdLogic, "layout.constraint.holdLogic");
  assertConfirmed(spec.typography.nature, "typography.nature");
  assertConfirmed(spec.typography.styleName, "typography.styleName");
  assertConfirmed(spec.typography.fontFamily, "typography.fontFamily");
  assertConfirmed(spec.typography.fontFace, "typography.fontFace");
  assertConfirmed(spec.typography.fontAssetRef, "typography.fontAssetRef");
  assertConfirmed(spec.typography.fontFileRef, "typography.fontFileRef");
  assertConfirmed(spec.typography.lineHeightMode, "typography.lineHeightMode");
  assertConfirmed(spec.typography.letterSpacingMode, "typography.letterSpacingMode");
  assertConfirmed(spec.typography.baselineBehavior, "typography.baselineBehavior");

  if (spec.typography.fallbackDetected) {
    throw new Error("Typography check failed: runtime fallback font detected");
  }
  if (!spec.typography.glyphCoverageConfirmed) {
    throw new Error("Typography check failed: glyph coverage is not confirmed");
  }
  if (!spec.repeatedInstanceGroup.allInstancesConfirmedIdentical) {
    throw new Error("Repeated instance consistency not confirmed");
  }
  if (spec.assetSources.some((asset) => !asset.exactMatchConfirmed)) {
    throw new Error("Asset source-of-truth not confirmed for all assets");
  }
}

export function PixelPerfectWebComponent({ spec }: { spec: PixelPerfectWebSpec }) {
  assertStrict(spec);

  return (
    <section
      data-root-frame={spec.rootFrameId}
      data-baseline-behavior={spec.typography.baselineBehavior}
      data-font-face={spec.typography.fontFace}
      data-font-source={spec.typography.fontFileRef}
      style={{
        width: spec.layout.width,
        height: spec.layout.height,
        marginTop: spec.layout.marginTop,
        marginRight: spec.layout.marginRight,
        marginBottom: spec.layout.marginBottom,
        marginLeft: spec.layout.marginLeft,
        paddingTop: spec.layout.paddingTop,
        paddingRight: spec.layout.paddingRight,
        paddingBottom: spec.layout.paddingBottom,
        paddingLeft: spec.layout.paddingLeft,
        display: "flex",
        flexDirection: "column",
        gap: spec.layout.gap,
        mixBlendMode: spec.compositing.blendMode === "other" ? "normal" : spec.compositing.blendMode,
        opacity: spec.compositing.localOpacity,
      }}
    >
      {spec.typography.nature === "semantic-text" ? (
        <p
          style={{
            margin: 0,
            width: spec.typography.textContainerWidth,
            minHeight: spec.typography.textContainerHeight,
            fontFamily: spec.typography.fontFamily,
            fontSize: spec.typography.fontSize,
            fontWeight: spec.typography.fontWeight,
            fontStyle: spec.typography.fontStyle,
            lineHeight: spec.typography.lineHeightMode === "auto" ? "normal" : `${spec.typography.lineHeight}px`,
            letterSpacing:
              spec.typography.letterSpacingMode === "percent"
                ? `${spec.typography.letterSpacing}%`
                : `${spec.typography.letterSpacing}px`,
            textAlign: spec.typography.textAlign,
            textTransform: spec.typography.textTransform,
            textDecoration: spec.typography.textDecoration,
            whiteSpace: spec.typography.wrappingBehavior,
          }}
        >
          {spec.typography.textValue}
        </p>
      ) : (
        <div aria-label="Non-semantic text layer must come from exact source asset" />
      )}
    </section>
  );
}
