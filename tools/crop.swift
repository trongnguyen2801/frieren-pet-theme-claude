// usage: swift crop.swift in out x y w h   (top-left origin)
import CoreImage
let a = CommandLine.arguments
let img = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!
let (x, y, w, h) = (Double(a[3])!, Double(a[4])!, Double(a[5])!, Double(a[6])!)
let r = CGRect(x: x, y: img.extent.height - y - h, width: w, height: h)
let out = img.cropped(to: r).transformed(by: CGAffineTransform(translationX: -r.minX, y: -r.minY))
try CIContext().writeJPEGRepresentation(of: out, to: URL(fileURLWithPath: a[2]), colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!,
  options: [kCGImageDestinationLossyCompressionQuality as CIImageRepresentationOption: 0.9])
