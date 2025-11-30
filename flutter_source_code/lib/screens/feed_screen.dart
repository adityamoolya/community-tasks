import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../services/feed_service.dart';
import '../models/post_model.dart';
import 'post_detail_screen.dart';

class FeedScreen extends StatefulWidget {
  const FeedScreen({super.key});

  @override
  State<FeedScreen> createState() => _FeedScreenState();
}

class _FeedScreenState extends State<FeedScreen> {
  final FeedService _feedService = FeedService();
  late Future<List<Post>> _feedFuture;

  @override
  void initState() {
    super.initState();
    _refreshFeed();
  }

  Future<void> _refreshFeed() async {
    setState(() {
      _feedFuture = _feedService.getFeed();
    });
  }

  Future<void> _openMap(double lat, double lng) async {
    final Uri url = Uri.parse(
        "https://www.google.com/maps/dir/?api=1&destination=$lat,$lng"
    );

    if (await canLaunchUrl(url)) {
      await launchUrl(url, mode: LaunchMode.externalApplication);
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text("Could not open Google Maps"))
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Community Reports")),
      floatingActionButton: FloatingActionButton(
        backgroundColor: const Color(0xFF2E7D32),
        onPressed: () {
          print("Navigate to Create Screen");
        },
        child: const Icon(Icons.add, color: Colors.white),
      ),

      body: RefreshIndicator(
        onRefresh: _refreshFeed,
        child: FutureBuilder<List<Post>>(
          future: _feedFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }

            if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return const Center(child: Text("No posts found."));
            }

            final posts = snapshot.data!;

            return ListView.separated(
              padding: const EdgeInsets.all(16),
              itemCount: posts.length,
              separatorBuilder: (_, __) => const SizedBox(height: 16),
              itemBuilder: (context, index) {
                return _buildFeedCard(posts[index]);
              },
            );
          },
        ),
      ),
    );
  }

  Widget _buildFeedCard(Post post) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => PostDetailScreen(post: post)),
          ).then((_) => _refreshFeed());
        },
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ClipRRect(
              borderRadius: const BorderRadius.vertical(top: Radius.circular(12)),
              child: Hero(
                tag: "post_img_${post.id}",
                child: Image.network(
                  post.imageUrl,
                  height: 200,
                  width: double.infinity,
                  fit: BoxFit.cover,
                  errorBuilder: (_, __, ___) =>
                      Container(height: 200, color: Colors.grey[200], child: const Icon(Icons.broken_image)),
                ),
              ),
            ),

            Padding(
              padding: const EdgeInsets.all(12.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      _getStatusChip(post.status),
                      const Spacer(),

                      IconButton(
                        icon: const Icon(Icons.directions, color: Colors.blue),
                        onPressed: () => _openMap(post.latitude, post.longitude),
                        tooltip: "Navigate",
                        visualDensity: VisualDensity.compact,
                      ),

                      const SizedBox(width: 8),
                      const Icon(Icons.comment_outlined, size: 18, color: Colors.grey),
                      const SizedBox(width: 4),
                      Text("${post.comments.length}", style: const TextStyle(color: Colors.grey)),
                    ],
                  ),

                  const SizedBox(height: 8),
                  Text(
                    post.caption ?? "No Caption",
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _getStatusChip(String status) {
    Color color;
    switch (status.toLowerCase()) {
      case 'completed':
        color = Colors.green;
        break;
      case 'pending':
        color = Colors.orange;
        break;
      default:
        color = Colors.blue;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        status.toUpperCase(),
        style: TextStyle(color: color, fontSize: 10, fontWeight: FontWeight.bold),
      ),
    );
  }
}
