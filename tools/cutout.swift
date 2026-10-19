// Cuts the foreground subjects out of an image with Vision.
// usage: swift cutout.swift <in.jpg> <outDir>
// Writes color.jpg and mask.png (cropped to the subjects' box) and cut.png (RGBA preview).
import AppKit
import CoreImage
import Vision

let input = URL(fileURLWithPath: CommandLine.arguments[1])
let outDir = URL(fileURLWithPath: CommandLine.arguments[2])
let image = CIImage(contentsOf: input)!
let handler = VNImageRequestHandler(ciImage: image)
let request = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([request])
guard let result = request.results?.first else {
    print("no subject found")
    exit(1)
}
print("instances:", result.allInstances.count)
let mask = CIImage(cvPixelBuffer: try result.generateScaledMaskForImage(forInstances: result.allInstances, from: handler))

// The subjects' bounding box, from an 8-bit copy of the mask.
let ctx = CIContext()
let w = Int(mask.extent.width), h = Int(mask.extent.height)
var px = [UInt8](repeating: 0, count: w * h)
ctx.render(mask, toBitmap: &px, rowBytes: w, bounds: mask.extent, format: .L8, colorSpace: nil)
var minX = w, minY = h, maxX = 0, maxY = 0
for y in 0..<h { for x in 0..<w where px[y * w + x] > 25 {
    minX = min(minX, x); maxX = max(maxX, x); minY = min(minY, y); maxY = max(maxY, y)
} }
// Rows of the bitmap run top to bottom; CoreImage's y runs bottom to top.
let pad = 4
let box = CGRect(x: max(0, minX - pad), y: max(0, h - 1 - maxY - pad),
                 width: min(w, maxX + pad) - max(0, minX - pad), height: min(h, maxY + pad) - max(0, minY - pad))
print("box:", box)

let srgb = CGColorSpace(name: CGColorSpace.sRGB)!
let gray = CGColorSpace(name: CGColorSpace.linearGray)!
func moved(_ i: CIImage) -> CIImage { i.cropped(to: box).transformed(by: CGAffineTransform(translationX: -box.minX, y: -box.minY)) }
// Fill the background with the subjects' own edge colour (white) so JPEG ringing at the mask edge stays light.
let flat = moved(image.applyingFilter("CIBlendWithMask", parameters: [
    "inputBackgroundImage": CIImage(color: .white).cropped(to: image.extent), "inputMaskImage": mask]))
try ctx.writeJPEGRepresentation(of: flat, to: outDir.appendingPathComponent("color.jpg"), colorSpace: srgb,
                                options: [kCGImageDestinationLossyCompressionQuality as CIImageRepresentationOption: 0.86])
try ctx.writePNGRepresentation(of: moved(mask), to: outDir.appendingPathComponent("mask.png"), format: .L8, colorSpace: gray)
let cut = moved(image.applyingFilter("CIBlendWithMask", parameters: [
    "inputBackgroundImage": CIImage(color: .clear).cropped(to: image.extent), "inputMaskImage": mask]))
try ctx.writePNGRepresentation(of: cut, to: outDir.appendingPathComponent("cut.png"), format: .RGBA8, colorSpace: srgb)
