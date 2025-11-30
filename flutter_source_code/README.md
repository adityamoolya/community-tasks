# 📱  CleanQuest  - Flutter Mobile App

The mobile frontend for the Community Task Force platform. Built with Flutter for cross-platform compatibility on iOS and Android.

---

## ✨ Features

### 🗺️ Interactive Map View
- Browse all open cleanup tasks on an interactive map
- See task locations with custom markers
- Tap markers to view task details
- Filter tasks by status (open, pending, completed)

### 📸 Image Capture & Upload
- Take photos directly from the app
- Select from gallery
- Automatic image optimization before upload
- Real-time upload progress indicators

### 🎮 Gamification
- Earn points for completed tasks (50 points per verified cleanup)
- View global leaderboard
- Track your personal statistics
- See your contribution history

### 👤 User Profiles
- Secure authentication (login/register)
- Personal dashboard with stats
- View created tasks vs. solved tasks
- Track total points earned

### 💬 Social Features
- Comment on tasks to coordinate with others
- Like tasks to show support
- Real-time status updates
- Task discussion threads

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Flutter SDK** 3.0.0 or higher
- **Dart SDK** 3.0.0 or higher
- **Android Studio** (for Android development)
- **Xcode** (for iOS development - macOS only)
- **VS Code** or **Android Studio** (recommended IDEs)

### Installation

#### 1. Install Flutter

**macOS:**
```bash
# Download Flutter SDK
git clone https://github.com/flutter/flutter.git -b stable

# Add to PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="$PATH:`pwd`/flutter/bin"

# Verify installation
flutter doctor
```

**Windows:**
- Download Flutter SDK from [flutter.dev](https://flutter.dev/docs/get-started/install/windows)
- Extract to `C:\src\flutter`
- Add `C:\src\flutter\bin` to PATH
- Run `flutter doctor` in CMD/PowerShell

**Linux:**
```bash
# Download and extract Flutter
cd ~
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:$HOME/flutter/bin"

# Install dependencies
sudo apt-get install clang cmake ninja-build pkg-config libgtk-3-dev

# Verify installation
flutter doctor
```

#### 2. Set Up Your IDE

**VS Code:**
```bash
# Install Flutter extension
code --install-extension Dart-Code.flutter
```

**Android Studio:**
- Install Flutter plugin: `File` → `Settings` → `Plugins` → Search "Flutter" → Install

#### 3. Set Up Android Emulator

```bash
# Open Android Studio
# Tools → AVD Manager → Create Virtual Device
# Select a device (e.g., Pixel 5)
# Download system image (e.g., API 33)
# Finish and start emulator

# Verify device is connected
flutter devices
```

#### 4. Set Up iOS Simulator (macOS only)

```bash
# Install Xcode from App Store
# Install command line tools
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch

# Open simulator
open -a Simulator

# Verify device is connected
flutter devices
```

---

## 🔧 Project Setup

### 1. Clone and Navigate

```bash
cd flutter_code
```

### 2. Install Dependencies

```bash
flutter pub get
```

This will install all packages defined in `pubspec.yaml`, including:
- `http` - API requests
- `provider` - State management
- `google_maps_flutter` - Map integration
- `image_picker` - Camera/gallery access
- `cached_network_image` - Image caching
- `geolocator` - Location services
- And more...

### 3. Configure API Endpoint

Create or edit `lib/config/api_config.dart`:

```dart
class ApiConfig {
  // For local development (backend running on your machine)
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android Emulator
  // static const String baseUrl = 'http://127.0.0.1:8000'; // iOS Simulator
  
  // For production (deployed backend)
  // static const String baseUrl = 'https://your-app.railway.app';
  
  // Cloudinary config (optional, if needed in frontend)
  static const String cloudinaryCloudName = 'your_cloud_name';
}
```

**Important Network Notes:**

| Environment | URL to Use |
|------------|-----------|
| Android Emulator | `http://10.0.2.2:8000` |
| iOS Simulator | `http://127.0.0.1:8000` or `http://localhost:8000` |
| Physical Device | `http://YOUR_COMPUTER_IP:8000` (e.g., `http://192.168.1.5:8000`) |
| Production | `https://your-backend-domain.com` |

### 4. Configure Permissions

**Android** (`android/app/src/main/AndroidManifest.xml`):
```xml
<manifest>
    <!-- Add these permissions -->
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
    <uses-permission android:name="android.permission.CAMERA"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    
    <application>
        <!-- Add Google Maps API Key -->
        <meta-data
            android:name="com.google.android.geo.API_KEY"
            android:value="YOUR_GOOGLE_MAPS_API_KEY"/>
    </application>
</manifest>
```

**iOS** (`ios/Runner/Info.plist`):
```xml
<dict>
    <!-- Add these permission descriptions -->
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>We need your location to show nearby cleanup tasks</string>
    
    <key>NSCameraUsageDescription</key>
    <string>We need camera access to take photos of cleanup tasks</string>
    
    <key>NSPhotoLibraryUsageDescription</key>
    <string>We need photo library access to upload task images</string>
</dict>
```

### 5. Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Maps SDK for Android" and "Maps SDK for iOS"
4. Create credentials → API Key
5. Add the key to Android and iOS config files (see step 4)

---

## 🏃 Running the App

### Development Mode

```bash
# Run on connected device/emulator
flutter run

# Run with specific device
flutter devices  # List available devices
flutter run -d <device_id>

# Run with hot reload (default)
flutter run

# Run in release mode (optimized)
flutter run --release
```

### Debug vs Release Modes

| Mode | Purpose | Performance | File Size |
|------|---------|-------------|-----------|
| Debug | Development, hot reload | Slower | Larger |
| Profile | Performance testing | Medium | Medium |
| Release | Production build | Fast | Optimized |

---

## 🏗️ Project Structure

```
flutter_code/
├── lib/
│   ├── main.dart                    # App entry point
│   ├── config/
│   │   └── api_config.dart          # API endpoint configuration
│   ├── models/
│   │   ├── user.dart                # User data model
│   │   ├── post.dart                # Task/post data model
│   │   └── comment.dart             # Comment data model
│   ├── services/
│   │   ├── api_service.dart         # HTTP API calls
│   │   ├── auth_service.dart        # Authentication logic
│   │   ├── image_service.dart       # Image upload handling
│   │   └── location_service.dart    # GPS location handling
│   ├── providers/
│   │   ├── auth_provider.dart       # Auth state management
│   │   ├── post_provider.dart       # Task state management
│   │   └── user_provider.dart       # User state management
│   ├── screens/
│   │   ├── auth/
│   │   │   ├── login_screen.dart
│   │   │   └── register_screen.dart
│   │   ├── home/
│   │   │   ├── home_screen.dart
│   │   │   └── map_screen.dart
│   │   ├── posts/
│   │   │   ├── create_post_screen.dart
│   │   │   ├── post_detail_screen.dart
│   │   │   └── submit_proof_screen.dart
│   │   └── profile/
│   │       ├── profile_screen.dart
│   │       └── leaderboard_screen.dart
│   ├── widgets/
│   │   ├── post_card.dart           # Reusable post display card
│   │   ├── comment_widget.dart      # Comment display widget
│   │   ├── custom_button.dart       # Styled buttons
│   │   └── loading_indicator.dart   # Loading animations
│   └── utils/
│       ├── constants.dart           # App-wide constants
│       ├── validators.dart          # Form validation
│       └── helpers.dart             # Utility functions
├── assets/
│   ├── images/                      # App images/icons
│   └── fonts/                       # Custom fonts
├── android/                         # Android-specific config
├── ios/                             # iOS-specific config
├── test/                            # Unit and widget tests
└── pubspec.yaml                     # Dependencies and assets
```

---

## 📦 Key Dependencies

### Core Packages
```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  provider: ^6.0.5              # Simple, powerful state management
  
  # Networking
  http: ^1.1.0                  # HTTP requests to backend API
  
  # Maps & Location
  google_maps_flutter: ^2.5.0   # Interactive map view
  geolocator: ^10.0.0           # GPS location services
  
  # Image Handling
  image_picker: ^1.0.4          # Camera and gallery access
  cached_network_image: ^3.3.0  # Efficient image caching
  image: ^4.0.0                 # Image processing
  
  # UI Components
  flutter_svg: ^2.0.9           # SVG support
  shimmer: ^3.0.0               # Loading animations
  
  # Storage
  shared_preferences: ^2.2.2    # Local key-value storage
  
  # Utilities
  intl: ^0.18.0                 # Date formatting
  timeago: ^3.5.0               # Human-readable timestamps
```

---

## 🎨 App Screens Overview

### Authentication Flow
1. **Splash Screen** - App loading and initial checks
2. **Login Screen** - Username/email and password login
3. **Register Screen** - New user account creation

### Main App Flow
1. **Home/Feed Screen** - List of all open tasks
2. **Map Screen** - Interactive map with task markers
3. **Create Task Screen** - Report new issues with photos
4. **Task Detail Screen** - View task info, comments, proof
5. **Submit Proof Screen** - Upload cleanup completion photos
6. **Profile Screen** - User stats and task history
7. **Leaderboard Screen** - Top contributors ranking

---

## 🔨 Building for Production

### Android APK

```bash
# Build release APK
flutter build apk --release

# Build app bundle (recommended for Play Store)
flutter build appbundle --release

# Output location:
# build/app/outputs/flutter-apk/app-release.apk
# build/app/outputs/bundle/release/app-release.aab
```

### iOS IPA (macOS only)

```bash
# Build for iOS
flutter build ios --release

# Open Xcode to archive and export
open ios/Runner.xcworkspace
```

Then in Xcode:
1. Select "Any iOS Device" as target
2. Product → Archive
3. Distribute App → App Store Connect

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/widget_test.dart

# Run with coverage
flutter test --coverage
```

### Widget Testing Example

```dart
testWidgets('Login button is present', (WidgetTester tester) async {
  await tester.pumpWidget(MyApp());
  expect(find.text('Login'), findsOneWidget);
});
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "Unable to connect to backend API"**
```bash
# Check backend is running
curl http://127.0.0.1:8000/

# Verify API URL in api_config.dart
# For Android emulator, use http://10.0.2.2:8000
# For iOS simulator, use http://127.0.0.1:8000
```

**2. "Google Maps not showing"**
- Verify API key is added to AndroidManifest.xml and Info.plist
- Check that Maps SDK is enabled in Google Cloud Console
- Ensure billing is enabled for the Google Cloud project

**3. "Camera/Location permission denied"**
- Add permission descriptions in AndroidManifest.xml and Info.plist
- Request permissions at runtime in the app
- Check device settings allow app permissions

**4. "Build failed: SDK version mismatch"**
```bash
# Update Flutter
flutter upgrade

# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

**5. "Hot reload not working"**
```bash
# Restart app with hot reload enabled
flutter run

# Or press 'r' in terminal for hot reload
# Press 'R' for hot restart
```

---

## 📱 Testing on Physical Device

### Android

1. **Enable Developer Options:**
   - Settings → About Phone → Tap "Build Number" 7 times

2. **Enable USB Debugging:**
   - Settings → Developer Options → USB Debugging

3. **Connect Device:**
   ```bash
   # Verify device is detected
   flutter devices
   
   # Run on device
   flutter run
   ```

### iOS (macOS only)

1. **Trust Developer Certificate:**
   - Connect iPhone via USB
   - Trust computer on device

2. **Configure Xcode:**
   - Open `ios/Runner.xcworkspace`
   - Select your team in Signing & Capabilities
   - Select your device

3. **Run:**
   ```bash
   flutter run
   ```

---

## 🚀 Publishing

### Google Play Store

1. **Prepare Release:**
   - Update version in `pubspec.yaml`
   - Generate signing key
   - Configure `android/app/build.gradle`

2. **Build:**
   ```bash
   flutter build appbundle --release
   ```

3. **Upload:**
   - Go to [Google Play Console](https://play.google.com/console)
   - Create app → Upload AAB file

### Apple App Store

1. **Prepare:**
   - Update version in Xcode
   - Configure signing

2. **Archive:**
   - Product → Archive in Xcode

3. **Upload:**
   - Distribute App → App Store Connect

---

## 🔐 Security Best Practices

- ✅ Store API keys in environment variables (not in code)
- ✅ Use HTTPS for all API communications
- ✅ Validate all user inputs
- ✅ Implement proper error handling
- ✅ Keep dependencies up to date
- ✅ Never commit sensitive data to version control

---

## 📊 Performance Optimization

- Use `const` constructors where possible
- Implement lazy loading for lists
- Cache images with `cached_network_image`
- Optimize image sizes before upload
- Use `ListView.builder` for long lists
- Profile app with `flutter run --profile`

---

## 🤝 Contributing

See main [README.md](../README.md) for contribution guidelines.

---

## 📚 Additional Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)
- [Provider Package Guide](https://pub.dev/packages/provider)
- [Google Maps Flutter Plugin](https://pub.dev/packages/google_maps_flutter)

---